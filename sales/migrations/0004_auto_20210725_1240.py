# Generated by Django 3.2.5 on 2021-07-25 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_auto_20210725_1218'),
    ]

    operations = [
        migrations.RenameField(
            model_name='csv',
            old_name='csv_name',
            new_name='csv_file',
        ),
        migrations.RemoveField(
            model_name='csv',
            name='activated',
        ),
    ]