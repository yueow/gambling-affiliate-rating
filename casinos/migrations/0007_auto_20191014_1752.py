# Generated by Django 2.2.5 on 2019-10-14 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casinos', '0006_auto_20191010_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casino',
            name='cashback',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Does it have cashback?'),
        ),
    ]
