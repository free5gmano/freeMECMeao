# Generated by Django 2.2 on 2022-08-11 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NSManagement', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nsdinfo',
            old_name='vnfPkgIds',
            new_name='appPkgIds',
        ),
    ]