from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from inventory.models.base import BaseModel


class ItemModel(BaseModel):
    """
    A Item that can be described and store somewhere ;)
    """
    description = RichTextUploadingField(
        config_name='ItemModel.description',
        verbose_name=_('ItemModel.description.verbose_name'),
        help_text=_('ItemModel.description.help_text')
    )
    fcc_id = models.CharField(
        max_length=20,
        blank=True, null=True,
        verbose_name=_('ItemModel.fcc_id.verbose_name'),
        help_text=_('ItemModel.fcc_id.help_text')
    )
    location = models.ForeignKey(
        'inventory.LocationModel',
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name=_('ItemModel.location.verbose_name'),
        help_text=_('ItemModel.location.help_text')
    )

    def __str__(self):
        if self.location_id is None:
            return self.name
        else:
            return f'{self.name} ({self.location})'

    class Meta:
        verbose_name = _('ItemModel.verbose_name')
        verbose_name_plural = _('ItemModel.verbose_name_plural')
