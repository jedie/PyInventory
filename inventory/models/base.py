import logging
import re
import time
import unicodedata
import uuid

import tagulous.models
from bx_django_utils.models.timetracking import TimetrackingBaseModel
from django.conf import settings
from django.db import models
from django.db.models import QuerySet
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
        help_text=_('BaseModel.id.help_text'),
    )
    user = models.ForeignKey(  # "Owner" of this entry
        settings.AUTH_USER_MODEL,
        related_name='+',
        on_delete=models.CASCADE,
        editable=False,  # Must be set automatically and never changed
        verbose_name=_('BaseModel.user.verbose_name'),
        help_text=_('BaseModel.user.help_text'),
    )
    name = models.CharField(
        max_length=255, verbose_name=_('BaseModel.name.verbose_name'), help_text=_('BaseModel.name.help_text')
    )
    tags = tagulous.models.TagField(
        blank=True,
        case_sensitive=False,
        force_lowercase=False,
        space_delimiter=False,
        max_count=10,
        verbose_name=_('BaseModel.tags.verbose_name'),
        help_text=_('BaseModel.tags.help_text'),
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


def nomalize_text(text):
    """
    >>> nomalize_text('Foo Bar 1 §$% äö-üß +')
    'foobar1aou'
    """
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'[^\w]', '', text)
    return text


def generate_path_str(path):
    """
    >>> generate_path_str(['Foo', 'B a  r', '1 §$% äö-üß +'])
    'foo 0 bar 0 1aou'
    """
    # The choice of the separator is very important for the correct sorting by the database!
    # Use 0, because this character is used for sorting and is the first character in the charset.
    # The spaces are only visual separators ;)
    return ' 0 '.join(nomalize_text(part) for part in path)


class ParentTreeModelManager(models.Manager):
    def update_tree_info(self) -> None:
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
                entry.path_str = generate_path_str(path)
                entry.level = len(path)

            self.bulk_update(entries, ['path', 'path_str', 'level'])

            duration = (time.monotonic() - start_time) * 1000
            logger.info('Update %i entries in %ims', len(entries), duration)

    def related_objects(self, instance: 'BaseParentTreeModel') -> QuerySet:
        """
        Returns a QuerySet with relation section of the tree
        """
        path = instance.path
        if path is None:
            # Not saved -> Can't have related objects ;)
            return self.none()

        root_entry = path[0]
        qs = self.all()
        qs = qs.filter(path__0=root_entry)
        return qs


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
            self.path_str = generate_path_str(self.path)
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
        abstract = True


class BaseAttachmentModel(BaseModel):
    """
    Base model to store files or images to Items
    """

    name = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name=_('BaseItemAttachmentModel.name.verbose_name'),
        help_text=_('BaseItemAttachmentModel.name.help_text'),
    )
    position = models.PositiveSmallIntegerField(
        # Note: Will be set in admin via adminsortable2
        # The JavaScript which performs the sorting is 1-indexed !
        default=0,
        blank=False,
        null=False,
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
