import logging
import time
import uuid

import tagulous.models
from bx_django_utils.models.timetracking import TimetrackingBaseModel
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from inventory.parent_tree import ValuesListTree
from inventory.string_utils import ltruncatechars


logger = logging.getLogger(__name__)


class BaseModel(TimetrackingBaseModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('BaseModel.id.verbose_name'),
        help_text=_('BaseModel.id.help_text')
    )
    user = models.ForeignKey(  # "Owner" of this entry
        settings.AUTH_USER_MODEL,
        related_name='+',
        on_delete=models.CASCADE,
        editable=False,  # Must be set automatically and never changed
        verbose_name=_('BaseModel.user.verbose_name'),
        help_text=_('BaseModel.user.help_text')
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('BaseModel.name.verbose_name'),
        help_text=_('BaseModel.name.help_text')
    )
    tags = tagulous.models.TagField(
        blank=True,
        case_sensitive=False,
        force_lowercase=False,
        space_delimiter=False,
        max_count=10,
        verbose_name=_('BaseModel.tags.verbose_name'),
        help_text=_('BaseModel.tags.help_text')
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class ParentTreeModelManager(models.Manager):
    def update_tree_info(self):
        start_time = time.monotonic()

        values = self.all().values('pk', 'name', 'parent__pk', 'path')
        tree = ValuesListTree(values=values)
        tree_path = tree.get_tree_path()
        logger.debug('Tree path: %r', tree_path)
        update_path_info = tree.get_update_path_info()

        duration = (time.monotonic() - start_time) * 1000
        logger.info('Get update_path_info: %r in %ims', update_path_info, duration)

        if not update_path_info:
            logger.info('No tree path changed, ok')
        else:
            start_time = time.monotonic()

            entries = self.filter(pk__in=update_path_info.keys())
            for entry in entries:
                path = update_path_info[entry.pk]
                entry.path = path
                entry.path_str = '/'.join(path)
                entry.level = len(path)

            self.bulk_update(entries, ['path', 'path_str', 'level'])

            duration = (time.monotonic() - start_time) * 1000
            logger.info('Update %i entries in %ims', len(entries), duration)


class BaseParentTreeModel(BaseModel):
    path = models.JSONField(
        blank=True,
        null=True,
        editable=False,
    )
    path_str = models.TextField(
        blank=True,
        null=True,
        editable=False,
    )
    level = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        editable=False,
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('LocationModel.parent.verbose_name'),
        help_text=_('LocationModel.parent.help_text'),
    )

    objects = models.Manager()
    tree_objects = ParentTreeModelManager()

    def save(self, **kwargs):
        if not self.path:
            if self.parent:
                path = self.parent.path
                if path:
                    self.path = [*path, self.name]
            else:
                self.path = [self.name]
            self.path_str = '/'.join(self.path)
            self.level = len(self.path)
            logger.info('Init path with: %r', self.path)

        self.full_clean()
        super().save(**kwargs)
        self.__class__.tree_objects.update_tree_info()

    def __str__(self):
        if self.path:
            text = ' › '.join(self.path)
            text = ltruncatechars(text, max_length=settings.TREE_PATH_STR_MAX_LENGTH)
            return text

        return self.name

    class Meta:
        ordering = ('path_str', 'name')
        abstract = True


class BaseAttachmentModel(BaseModel):
    """
    Base model to store files or images to Items
    """
    name = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_('BaseItemAttachmentModel.name.verbose_name'),
        help_text=_('BaseItemAttachmentModel.name.help_text')
    )
    position = models.PositiveSmallIntegerField(
        # Note: Will be set in admin via adminsortable2
        # The JavaScript which performs the sorting is 1-indexed !
        default=0, blank=False, null=False
    )

    def __str__(self):
        return self.name

    def full_clean(self, *, parent_instance, **kwargs):
        if self.user_id is None:
            # inherit owner of this link from parent model instance
            self.user_id = parent_instance.user_id

        return super().full_clean(**kwargs)

    class Meta:
        abstract = True


class BaseItemAttachmentModel(BaseAttachmentModel):
    """
    Base model to store files or images to Items
    """
    item = models.ForeignKey('ItemModel', on_delete=models.CASCADE)

    def full_clean(self, **kwargs):
        return super().full_clean(parent_instance=self.item, **kwargs)

    class Meta:
        abstract = True


class BaseMemoAttachmentModel(BaseAttachmentModel):
    """
    Base model to store files or images to Memos
    """
    memo = models.ForeignKey('MemoModel', on_delete=models.CASCADE)

    def full_clean(self, **kwargs):
        return super().full_clean(parent_instance=self.memo, **kwargs)

    class Meta:
        abstract = True
