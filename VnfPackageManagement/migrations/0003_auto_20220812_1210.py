# Generated by Django 2.2 on 2022-08-12 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VnfPackageManagement', '0002_auto_20220811_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='vnfpkginfo',
            name='appProductName',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vnfpkginfo',
            name='type',
            field=models.TextField(blank=True, null=True),
        ),
    ]
