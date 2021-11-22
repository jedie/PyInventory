import logging
from pathlib import Path

from bx_django_utils.filename import clean_filename
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_tools.model_version_protect.models import VersionProtectBaseModel
from django_tools.serve_media_app.models import user_directory_path

from inventory.models.base import BaseMemoAttachmentModel, BaseModel
from inventory.models.links import BaseLink


logger = logging.getLogger(__name__)


class MemoModel(BaseModel, VersionProtectBaseModel):
    """
    A Memo to hold some information independ of items/location
    """
    memo = RichTextUploadingField(
        blank=True, null=True,
        config_name='MemoModel.description',
        verbose_name=_('MemoModel.description.verbose_name'),
        help_text=_('MemoModel.description.help_text')
    )

    def local_admin_link(self):
        url = reverse('admin:inventory_memomodel_change', args=[self.id])
        return url

    class Meta:
        verbose_name = _('MemoModel.verbose_name')
        verbose_name_plural = _('MemoModel.verbose_name_plural')


class MemoLinkModel(BaseLink):
    memo = models.ForeignKey(
        MemoModel, on_delete=models.CASCADE
    )

    def full_clean(self, **kwargs):
        if self.user_id is None:
            # inherit owner of this link from item instance
            self.user_id = self.memo.user_id
        return super().full_clean(**kwargs)

    class Meta:
        verbose_name = _('MemoLinkModel.verbose_name')
        verbose_name_plural = _('MemoLinkModel.verbose_name_plural')
        ordering = ('position',)


class MemoImageModel(BaseMemoAttachmentModel):
    """
    Store images to Memos
    """
    image = models.ImageField(
        upload_to=user_directory_path,
        verbose_name=_('MemoImageModel.image.verbose_name'),
        help_text=_('MemoImageModel.image.help_text')
    )

    def __str__(self):
        return self.name or self.image.name

    def full_clean(self, **kwargs):
        # Set name by image filename:
        if not self.name:
            filename = Path(self.image.name).name
            self.name = clean_filename(filename)

        return super().full_clean(**kwargs)

    class Meta:
        verbose_name = _('MemoImageModel.verbose_name')
        verbose_name_plural = _('MemoImageModel.verbose_name_plural')
        ordering = ('position',)


class MemoFileModel(BaseMemoAttachmentModel):
    """
    Store files to Memos
    """
    file = models.FileField(
        upload_to=user_directory_path,
        verbose_name=_('MemoFileModel.file.verbose_name'),
        help_text=_('MemoFileModel.file.help_text')
    )

    def __str__(self):
        return self.name or self.file.name

    def full_clean(self, **kwargs):
        # Set name by filename:
        if not self.name:
            filename = Path(self.file.name).name
            self.name = clean_filename(filename)

        return super().full_clean(**kwargs)

    class Meta:
        verbose_name = _('MemoFileModel.verbose_name')
        verbose_name_plural = _('MemoFileModel.verbose_name_plural')
        ordering = ('position',)
