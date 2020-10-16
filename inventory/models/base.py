import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('ID')
    )
    create_dt = models.DateTimeField(
        blank=True,
        null=True,
        editable=False,
        verbose_name=_('BaseApproveModel.create_dt.verbose_name'),
        help_text=_('BaseApproveModel.create_dt.help_text')
    )
    update_dt = models.DateTimeField(
        blank=True,
        null=True,
        editable=False,
        verbose_name=_('BaseApproveModel.update_dt.verbose_name'),
        help_text=_('BaseApproveModel.update_dt.help_text')
    )

    def save(self, update_dt=True, **kwargs):
        if update_dt:
            if 'update_fields' in kwargs:
                update_fields = list(kwargs['update_fields'])
            else:
                update_fields = None

            self.update_dt = timezone.now()
            if update_fields:
                assert 'update_dt' not in update_fields
                update_fields.append('update_dt')

            if self.create_dt is None:
                self.create_dt = self.update_dt
                if update_fields:
                    assert 'create_dt' not in update_fields
                    update_fields.append('create_dt')

            if update_fields:
                kwargs['update_fields'] = update_fields

        self.full_clean()

        return super().save(**kwargs)

    class Meta:
        abstract = True
