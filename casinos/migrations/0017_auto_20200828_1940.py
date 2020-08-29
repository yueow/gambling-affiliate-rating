# Generated by Django 3.1 on 2020-08-28 19:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('casinos', '0016_auto_20200827_0031'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='casinorating',
            options={'verbose_name_plural': 'Casino Ratings'},
        ),
        migrations.AlterField(
            model_name='casinorating',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
