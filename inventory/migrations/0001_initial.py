# Generated by Django 2.2.16 on 2020-10-17 17:26

import uuid


import django.db.models.deletion
import tagulous.models.fields
import tagulous.models.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tagulous_LocationModel_tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                (
                    'count',
                    models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use'),
                ),
                (
                    'protected',
                    models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0'),
                ),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
                'unique_together': {('slug',)},
            },
            bases=(tagulous.models.models.BaseTagModel, models.Model),
        ),
        migrations.CreateModel(
            name='Tagulous_ItemModel_tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                (
                    'count',
                    models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use'),
                ),
                (
                    'protected',
                    models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0'),
                ),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
                'unique_together': {('slug',)},
            },
            bases=(tagulous.models.models.BaseTagModel, models.Model),
        ),
        migrations.CreateModel(
            name='Tagulous_ItemModel_producer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                (
                    'count',
                    models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use'),
                ),
                (
                    'protected',
                    models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0'),
                ),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
                'unique_together': {('slug',)},
            },
            bases=(tagulous.models.models.BaseTagModel, models.Model),
        ),
        migrations.CreateModel(
            name='Tagulous_ItemModel_kind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                (
                    'count',
                    models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use'),
                ),
                (
                    'protected',
                    models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0'),
                ),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
                'unique_together': {('slug',)},
            },
            bases=(tagulous.models.models.BaseTagModel, models.Model),
        ),
        migrations.CreateModel(
            name='Tagulous_ItemLinkModel_tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                (
                    'count',
                    models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use'),
                ),
                (
                    'protected',
                    models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0'),
                ),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
                'unique_together': {('slug',)},
            },
            bases=(tagulous.models.models.BaseTagModel, models.Model),
        ),
        migrations.CreateModel(
            name='Tagulous_BaseModel_tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                (
                    'count',
                    models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use'),
                ),
                (
                    'protected',
                    models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0'),
                ),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
                'unique_together': {('slug',)},
            },
            bases=(tagulous.models.models.BaseTagModel, models.Model),
        ),
        migrations.CreateModel(
            name='Tagulous_BaseLink_tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                (
                    'count',
                    models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use'),
                ),
                (
                    'protected',
                    models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0'),
                ),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
                'unique_together': {('slug',)},
            },
            bases=(tagulous.models.models.BaseTagModel, models.Model),
        ),
        migrations.CreateModel(
            name='LocationModel',
            fields=[
                (
                    'create_dt',
                    models.DateTimeField(
                        blank=True,
                        editable=False,
                        help_text='ModelTimetrackingMixin.create_dt.help_text',
                        null=True,
                        verbose_name='ModelTimetrackingMixin.create_dt.verbose_name',
                    ),
                ),
                (
                    'update_dt',
                    models.DateTimeField(
                        blank=True,
                        editable=False,
                        help_text='ModelTimetrackingMixin.update_dt.help_text',
                        null=True,
                        verbose_name='ModelTimetrackingMixin.update_dt.verbose_name',
                    ),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='BaseModel.id.help_text',
                        primary_key=True,
                        serialize=False,
                        verbose_name='BaseModel.id.verbose_name',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='BaseModel.name.help_text',
                        max_length=255,
                        verbose_name='BaseModel.name.verbose_name',
                    ),
                ),
                (
                    'description',
                    models.TextField(
                        help_text='LocationModel.description.help_text',
                        verbose_name='LocationModel.description.verbose_name',
                    ),
                ),
                (
                    'parent',
                    models.ForeignKey(
                        blank=True,
                        help_text='LocationModel.parent.help_text',
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to='inventory.LocationModel',
                        verbose_name='LocationModel.parent.verbose_name',
                    ),
                ),
                (
                    'tags',
                    tagulous.models.fields.TagField(
                        _set_tag_meta=True,
                        blank=True,
                        force_lowercase=False,
                        help_text='BaseModel.tags.help_text',
                        max_count=10,
                        to='inventory.Tagulous_LocationModel_tags',
                        verbose_name='BaseModel.tags.verbose_name',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        editable=False,
                        help_text='BaseModel.user.help_text',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='+',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='BaseModel.user.verbose_name',
                    ),
                ),
            ],
            options={
                'verbose_name': 'LocationModel.verbose_name',
                'verbose_name_plural': 'LocationModel.verbose_name_plural',
            },
        ),
        migrations.CreateModel(
            name='ItemModel',
            fields=[
                (
                    'create_dt',
                    models.DateTimeField(
                        blank=True,
                        editable=False,
                        help_text='ModelTimetrackingMixin.create_dt.help_text',
                        null=True,
                        verbose_name='ModelTimetrackingMixin.create_dt.verbose_name',
                    ),
                ),
                (
                    'update_dt',
                    models.DateTimeField(
                        blank=True,
                        editable=False,
                        help_text='ModelTimetrackingMixin.update_dt.help_text',
                        null=True,
                        verbose_name='ModelTimetrackingMixin.update_dt.verbose_name',
                    ),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='BaseModel.id.help_text',
                        primary_key=True,
                        serialize=False,
                        verbose_name='BaseModel.id.verbose_name',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='BaseModel.name.help_text',
                        max_length=255,
                        verbose_name='BaseModel.name.verbose_name',
                    ),
                ),
                (
                    'description',
                    models.TextField(
                        blank=True,
                        help_text='ItemModel.description.help_text',
                        null=True,
                        verbose_name='ItemModel.description.verbose_name',
                    ),
                ),
                (
                    'fcc_id',
                    models.CharField(
                        blank=True,
                        help_text='ItemModel.fcc_id.help_text',
                        max_length=20,
                        null=True,
                        verbose_name='ItemModel.fcc_id.verbose_name',
                    ),
                ),
                (
                    'lent_to',
                    models.CharField(
                        blank=True,
                        help_text='ItemModel.lent_to.help_text',
                        max_length=64,
                        null=True,
                        verbose_name='ItemModel.lent_to.verbose_name',
                    ),
                ),
                (
                    'lent_from_date',
                    models.DateField(
                        blank=True,
                        help_text='ItemModel.lent_from_date.help_text',
                        null=True,
                        verbose_name='ItemModel.lent_from_date.verbose_name',
                    ),
                ),
                (
                    'lent_until_date',
                    models.DateField(
                        blank=True,
                        help_text='ItemModel.lent_until_date.help_text',
                        null=True,
                        verbose_name='ItemModel.lent_until_date.verbose_name',
                    ),
                ),
                (
                    'received_from',
                    models.CharField(
                        blank=True,
                        help_text='ItemModel.received_from.help_text',
                        max_length=64,
                        null=True,
                        verbose_name='ItemModel.received_from.verbose_name',
                    ),
                ),
                (
                    'received_date',
                    models.DateField(
                        blank=True,
                        help_text='ItemModel.received_date.help_text',
                        null=True,
                        verbose_name='ItemModel.received_date.verbose_name',
                    ),
                ),
                (
                    'received_price',
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text='ItemModel.received_price.help_text',
                        max_digits=6,
                        null=True,
                        verbose_name='ItemModel.received_price.verbose_name',
                    ),
                ),
                (
                    'handed_over_to',
                    models.CharField(
                        blank=True,
                        help_text='ItemModel.handed_over_to.help_text',
                        max_length=64,
                        null=True,
                        verbose_name='ItemModel.handed_over_to.verbose_name',
                    ),
                ),
                (
                    'handed_over_date',
                    models.DateField(
                        blank=True,
                        help_text='ItemModel.handed_over_date.help_text',
                        null=True,
                        verbose_name='ItemModel.handed_over_date.verbose_name',
                    ),
                ),
                (
                    'handed_over_price',
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text='ItemModel.handed_over_price.help_text',
                        max_digits=6,
                        null=True,
                        verbose_name='ItemModel.handed_over_price.verbose_name',
                    ),
                ),
                (
                    'kind',
                    tagulous.models.fields.TagField(
                        _set_tag_meta=True,
                        force_lowercase=False,
                        help_text='ItemModel.kind.help_text',
                        max_count=3,
                        to='inventory.Tagulous_ItemModel_kind',
                        verbose_name='ItemModel.kind.verbose_name',
                    ),
                ),
                (
                    'location',
                    models.ForeignKey(
                        blank=True,
                        help_text='ItemModel.location.help_text',
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to='inventory.LocationModel',
                        verbose_name='ItemModel.location.verbose_name',
                    ),
                ),
                (
                    'parent',
                    models.ForeignKey(
                        blank=True,
                        help_text='ItemModel.parent.help_text',
                        limit_choices_to={'parent_id': None},
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to='inventory.ItemModel',
                        verbose_name='ItemModel.parent.verbose_name',
                    ),
                ),
                (
                    'producer',
                    tagulous.models.fields.TagField(
                        _set_tag_meta=True,
                        blank=True,
                        force_lowercase=False,
                        help_text='ItemModel.producer.help_text',
                        max_count=1,
                        to='inventory.Tagulous_ItemModel_producer',
                        verbose_name='ItemModel.producer.verbose_name',
                    ),
                ),
                (
                    'tags',
                    tagulous.models.fields.TagField(
                        _set_tag_meta=True,
                        blank=True,
                        force_lowercase=False,
                        help_text='BaseModel.tags.help_text',
                        max_count=10,
                        to='inventory.Tagulous_ItemModel_tags',
                        verbose_name='BaseModel.tags.verbose_name',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        editable=False,
                        help_text='BaseModel.user.help_text',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='+',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='BaseModel.user.verbose_name',
                    ),
                ),
            ],
            options={
                'verbose_name': 'ItemModel.verbose_name',
                'verbose_name_plural': 'ItemModel.verbose_name_plural',
            },
        ),
        migrations.CreateModel(
            name='ItemLinkModel',
            fields=[
                (
                    'create_dt',
                    models.DateTimeField(
                        blank=True,
                        editable=False,
                        help_text='ModelTimetrackingMixin.create_dt.help_text',
                        null=True,
                        verbose_name='ModelTimetrackingMixin.create_dt.verbose_name',
                    ),
                ),
                (
                    'update_dt',
                    models.DateTimeField(
                        blank=True,
                        editable=False,
                        help_text='ModelTimetrackingMixin.update_dt.help_text',
                        null=True,
                        verbose_name='ModelTimetrackingMixin.update_dt.verbose_name',
                    ),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text='BaseModel.id.help_text',
                        primary_key=True,
                        serialize=False,
                        verbose_name='BaseModel.id.verbose_name',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        blank=True,
                        help_text='BaseLink.name.help_text',
                        max_length=255,
                        null=True,
                        verbose_name='BaseLink.name.verbose_name',
                    ),
                ),
                ('url', models.URLField(help_text='Link.url.help_text', verbose_name='Link.url.verbose_name')),
                (
                    'last_check',
                    models.DateField(
                        blank=True,
                        editable=False,
                        help_text='Link.url.help_text',
                        null=True,
                        verbose_name='Link.url.verbose_name',
                    ),
                ),
                (
                    'status_code',
                    models.PositiveSmallIntegerField(
                        blank=True,
                        editable=False,
                        help_text='Link.status_code.help_text',
                        null=True,
                        verbose_name='Link.status_code.verbose_name',
                    ),
                ),
                (
                    'page_title',
                    models.CharField(
                        blank=True,
                        editable=False,
                        help_text='Link.page_title.help_text',
                        max_length=255,
                        null=True,
                        verbose_name='Link.page_title.verbose_name',
                    ),
                ),
                ('position', models.PositiveSmallIntegerField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.ItemModel')),
                (
                    'tags',
                    tagulous.models.fields.TagField(
                        _set_tag_meta=True,
                        blank=True,
                        force_lowercase=False,
                        help_text='BaseModel.tags.help_text',
                        max_count=10,
                        to='inventory.Tagulous_ItemLinkModel_tags',
                        verbose_name='BaseModel.tags.verbose_name',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        editable=False,
                        help_text='BaseModel.user.help_text',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='+',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='BaseModel.user.verbose_name',
                    ),
                ),
            ],
            options={
                'verbose_name': 'ItemLinkModel.verbose_name',
                'verbose_name_plural': 'ItemLinkModel.verbose_name_plural',
                'ordering': ('position',),
            },
        ),
    ]
