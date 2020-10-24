from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from inventory.models.base import BaseModel


class LocationModel(BaseModel):
    """
    A Storage for items.
    """
    description = RichTextUploadingField(
        blank=True, null=True,
        config_name='LocationModel.description',
        verbose_name=_('LocationModel.description.verbose_name'),
        help_text=_('LocationModel.description.help_text')
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_('LocationModel.parent.verbose_name'),
        help_text=_('LocationModel.parent.help_text')
    )

    def __str__(self):
        if self.parent_id is None:
            return self.name
        else:
            return f'{self.name} › {self.parent}'

    class Meta:
        verbose_name = _('LocationModel.verbose_name')
        verbose_name_plural = _('LocationModel.verbose_name_plural')
