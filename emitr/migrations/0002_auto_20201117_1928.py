# Generated by Django 3.1.2 on 2020-11-17 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emitr', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='CustomUser',
        ),
    ]
