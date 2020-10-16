from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from inventory.models.base import BaseModel


class ItemModel(BaseModel):
    """
    A Item that can be described and store somewhere ;)
    """
    description = RichTextUploadingField(
        config_name='ItemModel.description'
    )
    fcc_id = models.CharField(
        max_length=20,
        blank=True, null=True,
        verbose_name='FCC ID',
        help_text=_('FCC ID-Number for links to: https://fccid.io/')
    )
