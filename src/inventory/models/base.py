import uuid

import tagulous.models
from bx_django_utils.models.timetracking import TimetrackingBaseModel
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


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


class BaseItemAttachmentModel(BaseModel):
    """
    Base model to store files or images to Items
    """
    name = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_('BaseItemAttachmentModel.name.verbose_name'),
        help_text=_('BaseItemAttachmentModel.name.help_text')
    )
    item = models.ForeignKey('ItemModel', on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField(
        # Note: Will be set in admin via adminsortable2
        # The JavaScript which performs the sorting is 1-indexed !
        default=0, blank=False, null=False
    )

    def __str__(self):
        return self.name

    def full_clean(self, **kwargs):
        if self.user_id is None:
            # inherit owner of this link from item instance
            self.user_id = self.item.user_id

        return super().full_clean(**kwargs)

    class Meta:
        abstract = True
