# Generated by Django 2.2.5 on 2019-10-12 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_delete_casino'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='time_for_reading',
            field=models.CharField(max_length=50, null=True, verbose_name="Time for reading('2 минуты')"),
        ),
    ]