# Generated by Django 3.1 on 2020-08-27 00:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('casinos', '0015_auto_20200825_2041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='casino',
            name='cons_c',
        ),
        migrations.RemoveField(
            model_name='casino',
            name='pros_c',
        ),
        migrations.CreateModel(
            name='CasinoRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(decimal_places=1, default=0, max_digits=3, verbose_name='Main rate')),
                ('rate_soft', models.DecimalField(decimal_places=1, default=0, max_digits=3, verbose_name='Software Rate')),
                ('rate_design', models.DecimalField(decimal_places=1, default=0, max_digits=3, verbose_name='Design Rate')),
                ('rate_safe', models.DecimalField(decimal_places=1, default=0, max_digits=3, verbose_name='Safe Rate')),
                ('rate_faith', models.DecimalField(decimal_places=1, default=0, max_digits=3, verbose_name='Faith Rate')),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
                ('casino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='casinos.casino')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
