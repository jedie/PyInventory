from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django_prose_editor.sanitized import SanitizedProseEditorField
from django_tools.model_version_protect.models import VersionProtectBaseModel

from inventory.models.base import BaseParentTreeModel


class LocationModel(BaseParentTreeModel, VersionProtectBaseModel):
    """
    A Storage for items.
    """

    description = SanitizedProseEditorField(
        blank=True,
        null=True,
        config=settings.PROSE_EDITOR_DEFAULT_CONFIG,
        verbose_name=_('LocationModel.description.verbose_name'),
        help_text=_('LocationModel.description.help_text'),
    )

    class Meta:
        ordering = ('path_str',)
        verbose_name = _('LocationModel.verbose_name')
        verbose_name_plural = _('LocationModel.verbose_name_plural')
