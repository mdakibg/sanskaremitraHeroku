# Generated by Django 3.1.2 on 2020-12-30 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emitr', '0022_auto_20201230_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subservice',
            name='fee',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='subservice',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.DeleteModel(
            name='ServiceImage',
        ),
    ]
