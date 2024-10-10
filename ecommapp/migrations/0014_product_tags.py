# Generated by Django 5.1.1 on 2024-10-08 19:50

import taggit.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0013_product_expiry_product_mfg_product_stock_and_more'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]