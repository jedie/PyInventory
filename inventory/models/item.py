import tagulous.models
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from inventory.models.base import BaseModel
from inventory.models.links import BaseLink


class ItemQuerySet(models.QuerySet):
    def sort(self):
        return self.order_by('kind', 'producer', 'name')


class ItemModel(BaseModel):
    """
    A Item that can be described and store somewhere ;)
    """
    objects = ItemQuerySet.as_manager()

    kind = tagulous.models.TagField(
        case_sensitive=False,
        force_lowercase=False,
        space_delimiter=False,
        max_count=3,
        verbose_name=_('ItemModel.kind.verbose_name'),
        help_text=_('ItemModel.kind.help_text')
    )
    producer = tagulous.models.TagField(
        blank=True,
        case_sensitive=False,
        force_lowercase=False,
        space_delimiter=False,
        max_count=1,
        verbose_name=_('ItemModel.producer.verbose_name'),
        help_text=_('ItemModel.producer.help_text')
    )
    description = RichTextUploadingField(
        blank=True, null=True,
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
    parent = models.ForeignKey(
        'self',
        limit_choices_to={'parent_id': None},
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_('ItemModel.parent.verbose_name'),
        help_text=_('ItemModel.parent.help_text')
    )

    # ________________________________________________________________________
    # lent

    lent_to = models.CharField(
        max_length=64,
        blank=True, null=True,
        verbose_name=_('ItemModel.lent_to.verbose_name'),
        help_text=_('ItemModel.lent_to.help_text')
    )
    lent_from_date = models.DateField(
        blank=True, null=True,
        verbose_name=_('ItemModel.lent_from_date.verbose_name'),
        help_text=_('ItemModel.lent_from_date.help_text')
    )
    lent_until_date = models.DateField(
        blank=True, null=True,
        verbose_name=_('ItemModel.lent_until_date.verbose_name'),
        help_text=_('ItemModel.lent_until_date.help_text')
    )

    # ________________________________________________________________________
    # received

    received_from = models.CharField(
        max_length=64,
        blank=True, null=True,
        verbose_name=_('ItemModel.received_from.verbose_name'),
        help_text=_('ItemModel.received_from.help_text')
    )
    received_date = models.DateField(
        blank=True, null=True,
        verbose_name=_('ItemModel.received_date.verbose_name'),
        help_text=_('ItemModel.received_date.help_text')
    )
    received_price = models.DecimalField(
        decimal_places=2, max_digits=6,  # up to 9999 with a resolution of 2 decimal places
        blank=True, null=True,
        verbose_name=_('ItemModel.received_price.verbose_name'),
        help_text=_('ItemModel.received_price.help_text')
    )

    # ________________________________________________________________________
    # handed over

    handed_over_to = models.CharField(
        max_length=64,
        blank=True, null=True,
        verbose_name=_('ItemModel.handed_over_to.verbose_name'),
        help_text=_('ItemModel.handed_over_to.help_text')
    )
    handed_over_date = models.DateField(
        blank=True, null=True,
        verbose_name=_('ItemModel.handed_over_date.verbose_name'),
        help_text=_('ItemModel.handed_over_date.help_text')
    )
    handed_over_price = models.DecimalField(
        decimal_places=2, max_digits=6,  # up to 9999 with a resolution of 2 decimal places
        blank=True, null=True,
        verbose_name=_('ItemModel.handed_over_price.verbose_name'),
        help_text=_('ItemModel.handed_over_price.help_text')
    )

    def local_admin_link(self):
        url = reverse('admin:inventory_itemmodel_change', args=[self.id])
        return url

    def verbose_name(self):
        parts = [str(part) for part in (self.kind, self.producer, self.name)]
        return ' - '.join(part for part in parts if part)

    def __str__(self):
        if self.parent_id is None:
            title = self.name
        else:
            title = f'{self.name} › {self.parent}'

        if self.producer:
            title = f'{self.producer} - {title}'

        if self.location_id is not None:
            title = f'{title} ({self.location})'

        return title

    class Meta:
        verbose_name = _('ItemModel.verbose_name')
        verbose_name_plural = _('ItemModel.verbose_name_plural')


class ItemLinkModel(BaseLink):
    item = models.ForeignKey(
        ItemModel, on_delete=models.CASCADE
    )

    def full_clean(self, **kwargs):
        if self.user_id is None:
            # inherit owner of this link from item instance
            self.user_id = self.item.user_id
        return super().full_clean(**kwargs)

    class Meta:
        verbose_name = _('ItemLinkModel.verbose_name')
        verbose_name_plural = _('ItemLinkModel.verbose_name_plural')
        ordering = ('position',)
