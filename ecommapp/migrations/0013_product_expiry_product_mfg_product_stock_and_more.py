# Generated by Django 5.1.1 on 2024-10-08 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0012_alter_productimage_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='expiry',
            field=models.CharField(blank=True, default='10 Days', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='mfg',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.CharField(blank=True, default='0', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.CharField(blank=True, default='organic', max_length=100, null=True),
        ),
    ]
