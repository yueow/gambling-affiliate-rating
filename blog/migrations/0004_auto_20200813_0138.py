# Generated by Django 3.0.4 on 2020-08-13 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200813_0129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentrate',
            name='rate',
            field=models.CharField(choices=[('L', 'Like'), ('D', 'Disike')], default='L', max_length=10),
        ),
    ]
