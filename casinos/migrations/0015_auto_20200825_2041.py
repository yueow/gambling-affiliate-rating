# Generated by Django 3.1 on 2020-08-25 20:41

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casinos', '0014_auto_20200825_2019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feature',
            name='casino',
        ),
        migrations.AddField(
            model_name='casino',
            name='feature',
            field=models.ManyToManyField(related_name='features', to='casinos.Feature'),
        ),
        migrations.AlterField(
            model_name='casino',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='title'),
        ),
    ]
