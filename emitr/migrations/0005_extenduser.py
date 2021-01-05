# Generated by Django 3.1.2 on 2020-11-18 09:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('emitr', '0004_delete_extenduser'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=13)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mobile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]