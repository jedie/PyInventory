from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _
from django_tools.model_version_protect.models import VersionProtectBaseModel

from inventory.models.base import BaseParentTreeModel


class LocationModel(BaseParentTreeModel, VersionProtectBaseModel):
    """
    A Storage for items.
    """

    description = RichTextUploadingField(
        blank=True,
        null=True,
        config_name='LocationModel.description',
        verbose_name=_('LocationModel.description.verbose_name'),
        help_text=_('LocationModel.description.help_text'),
    )

    class Meta:
        ordering = ('path_str',)
        verbose_name = _('LocationModel.verbose_name')
        verbose_name_plural = _('LocationModel.verbose_name_plural')
