# Generated by Django 3.1.13 on 2021-10-09 17:38

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_tools.serve_media_app.models
import tagulous.models.fields
import tagulous.models.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0008_last_check_datetime'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tagulous_MemoModel_tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                ('count', models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use')),
                ('protected', models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
                'unique_together': {('slug',)},
            },
            bases=(tagulous.models.models.BaseTagModel, models.Model),
        ),
        migrations.CreateModel(
            name='Tagulous_MemoLinkModel_tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                ('count', models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use')),
                ('protected', models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
                'unique_together': {('slug',)},
            },
            bases=(tagulous.models.models.BaseTagModel, models.Model),
        ),
        migrations.CreateModel(
            name='Tagulous_MemoImageModel_tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                ('count', models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use')),
                ('protected', models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
                'unique_together': {('slug',)},
            },
            bases=(tagulous.models.models.BaseTagModel, models.Model),
        ),
        migrations.CreateModel(
            name='Tagulous_MemoFileModel_tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                ('count', models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use')),
                ('protected', models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
                'unique_together': {('slug',)},
            },
            bases=(tagulous.models.models.BaseTagModel, models.Model),
        ),
        migrations.CreateModel(
            name='Tagulous_BaseMemoAttachmentModel_tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                ('count', models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use')),
                ('protected', models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
                'unique_together': {('slug',)},
            },
            bases=(tagulous.models.models.BaseTagModel, models.Model),
        ),
        migrations.CreateModel(
            name='Tagulous_BaseAttachmentModel_tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                ('count', models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use')),
                ('protected', models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
                'unique_together': {('slug',)},
            },
            bases=(tagulous.models.models.BaseTagModel, models.Model),
        ),
        migrations.CreateModel(
            name='MemoModel',
            fields=[
                ('create_dt', models.DateTimeField(blank=True, editable=False, help_text='ModelTimetrackingMixin.create_dt.help_text', null=True, verbose_name='ModelTimetrackingMixin.create_dt.verbose_name')),
                ('update_dt', models.DateTimeField(blank=True, editable=False, help_text='ModelTimetrackingMixin.update_dt.help_text', null=True, verbose_name='ModelTimetrackingMixin.update_dt.verbose_name')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='BaseModel.id.help_text', primary_key=True, serialize=False, verbose_name='BaseModel.id.verbose_name')),
                ('name', models.CharField(help_text='BaseModel.name.help_text', max_length=255, verbose_name='BaseModel.name.verbose_name')),
                ('memo', ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='MemoModel.description.help_text', null=True, verbose_name='MemoModel.description.verbose_name')),
                ('tags', tagulous.models.fields.TagField(_set_tag_meta=True, blank=True, case_sensitive=False, force_lowercase=False, help_text='BaseModel.tags.help_text', max_count=10, space_delimiter=False, to='inventory.Tagulous_MemoModel_tags', verbose_name='BaseModel.tags.verbose_name')),
                ('user', models.ForeignKey(editable=False, help_text='BaseModel.user.help_text', on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='BaseModel.user.verbose_name')),
            ],
            options={
                'verbose_name': 'MemoModel.verbose_name',
                'verbose_name_plural': 'MemoModel.verbose_name_plural',
            },
        ),
        migrations.CreateModel(
            name='MemoLinkModel',
            fields=[
                ('create_dt', models.DateTimeField(blank=True, editable=False, help_text='ModelTimetrackingMixin.create_dt.help_text', null=True, verbose_name='ModelTimetrackingMixin.create_dt.verbose_name')),
                ('update_dt', models.DateTimeField(blank=True, editable=False, help_text='ModelTimetrackingMixin.update_dt.help_text', null=True, verbose_name='ModelTimetrackingMixin.update_dt.verbose_name')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='BaseModel.id.help_text', primary_key=True, serialize=False, verbose_name='BaseModel.id.verbose_name')),
                ('name', models.CharField(blank=True, help_text='BaseLink.name.help_text', max_length=255, null=True, verbose_name='BaseLink.name.verbose_name')),
                ('url', models.URLField(help_text='Link.url.help_text', verbose_name='Link.url.verbose_name')),
                ('last_check', models.DateTimeField(blank=True, editable=False, help_text='Link.url.help_text', null=True, verbose_name='Link.url.verbose_name')),
                ('status_code', models.PositiveSmallIntegerField(blank=True, editable=False, help_text='Link.status_code.help_text', null=True, verbose_name='Link.status_code.verbose_name')),
                ('page_title', models.CharField(blank=True, editable=False, help_text='Link.page_title.help_text', max_length=255, null=True, verbose_name='Link.page_title.verbose_name')),
                ('position', models.PositiveSmallIntegerField(default=0)),
                ('memo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.memomodel')),
                ('tags', tagulous.models.fields.TagField(_set_tag_meta=True, blank=True, case_sensitive=False, force_lowercase=False, help_text='BaseModel.tags.help_text', max_count=10, space_delimiter=False, to='inventory.Tagulous_MemoLinkModel_tags', verbose_name='BaseModel.tags.verbose_name')),
                ('user', models.ForeignKey(editable=False, help_text='BaseModel.user.help_text', on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='BaseModel.user.verbose_name')),
            ],
            options={
                'verbose_name': 'MemoLinkModel.verbose_name',
                'verbose_name_plural': 'MemoLinkModel.verbose_name_plural',
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='MemoImageModel',
            fields=[
                ('create_dt', models.DateTimeField(blank=True, editable=False, help_text='ModelTimetrackingMixin.create_dt.help_text', null=True, verbose_name='ModelTimetrackingMixin.create_dt.verbose_name')),
                ('update_dt', models.DateTimeField(blank=True, editable=False, help_text='ModelTimetrackingMixin.update_dt.help_text', null=True, verbose_name='ModelTimetrackingMixin.update_dt.verbose_name')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='BaseModel.id.help_text', primary_key=True, serialize=False, verbose_name='BaseModel.id.verbose_name')),
                ('name', models.CharField(blank=True, help_text='BaseItemAttachmentModel.name.help_text', max_length=255, null=True, verbose_name='BaseItemAttachmentModel.name.verbose_name')),
                ('position', models.PositiveSmallIntegerField(default=0)),
                ('image', models.ImageField(help_text='MemoImageModel.image.help_text', upload_to=django_tools.serve_media_app.models.user_directory_path, verbose_name='MemoImageModel.image.verbose_name')),
                ('memo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.memomodel')),
                ('tags', tagulous.models.fields.TagField(_set_tag_meta=True, blank=True, case_sensitive=False, force_lowercase=False, help_text='BaseModel.tags.help_text', max_count=10, space_delimiter=False, to='inventory.Tagulous_MemoImageModel_tags', verbose_name='BaseModel.tags.verbose_name')),
                ('user', models.ForeignKey(editable=False, help_text='BaseModel.user.help_text', on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='BaseModel.user.verbose_name')),
            ],
            options={
                'verbose_name': 'MemoImageModel.verbose_name',
                'verbose_name_plural': 'MemoImageModel.verbose_name_plural',
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='MemoFileModel',
            fields=[
                ('create_dt', models.DateTimeField(blank=True, editable=False, help_text='ModelTimetrackingMixin.create_dt.help_text', null=True, verbose_name='ModelTimetrackingMixin.create_dt.verbose_name')),
                ('update_dt', models.DateTimeField(blank=True, editable=False, help_text='ModelTimetrackingMixin.update_dt.help_text', null=True, verbose_name='ModelTimetrackingMixin.update_dt.verbose_name')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='BaseModel.id.help_text', primary_key=True, serialize=False, verbose_name='BaseModel.id.verbose_name')),
                ('name', models.CharField(blank=True, help_text='BaseItemAttachmentModel.name.help_text', max_length=255, null=True, verbose_name='BaseItemAttachmentModel.name.verbose_name')),
                ('position', models.PositiveSmallIntegerField(default=0)),
                ('file', models.FileField(help_text='MemoFileModel.file.help_text', upload_to=django_tools.serve_media_app.models.user_directory_path, verbose_name='MemoFileModel.file.verbose_name')),
                ('memo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.memomodel')),
                ('tags', tagulous.models.fields.TagField(_set_tag_meta=True, blank=True, case_sensitive=False, force_lowercase=False, help_text='BaseModel.tags.help_text', max_count=10, space_delimiter=False, to='inventory.Tagulous_MemoFileModel_tags', verbose_name='BaseModel.tags.verbose_name')),
                ('user', models.ForeignKey(editable=False, help_text='BaseModel.user.help_text', on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='BaseModel.user.verbose_name')),
            ],
            options={
                'verbose_name': 'MemoFileModel.verbose_name',
                'verbose_name_plural': 'MemoFileModel.verbose_name_plural',
                'ordering': ('position',),
            },
        ),
    ]