# Generated by Django 2.2.5 on 2019-10-05 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casinos', '0003_auto_20191005_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='casino',
            field=models.ManyToManyField(blank=True, to='casinos.Casino'),
        ),
    ]
