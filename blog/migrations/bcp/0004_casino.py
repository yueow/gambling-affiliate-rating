# Generated by Django 2.2.5 on 2019-09-14 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20190911_0522'),
    ]

    operations = [
        migrations.CreateModel(
            name='Casino',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Casino label')),
                ('country', models.CharField(blank=True, max_length=100, verbose_name='Country of casino')),
                ('ca_license', models.CharField(default='No', max_length=100, verbose_name='License')),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('dol', models.DateField(verbose_name='Date of launching')),
                ('image', models.ImageField(blank=True, upload_to='casino_logo', verbose_name='Logo')),
                ('rate_soft', models.DecimalField(decimal_places=1, default=0, max_digits=3, verbose_name='Main rate')),
                ('rate_design', models.DecimalField(decimal_places=1, default=0, max_digits=3, verbose_name='Design rate')),
                ('rate_safe', models.DecimalField(decimal_places=1, default=0, max_digits=3, verbose_name='Safe rate')),
                ('rate_faith', models.DecimalField(decimal_places=1, default=0, max_digits=3, verbose_name='Faith rate')),
                ('rate', models.DecimalField(decimal_places=1, default=0, max_digits=3, verbose_name='Main rate')),
                ('content', models.TextField(blank=True)),
                ('pros_c', models.TextField(blank=True, verbose_name='Pros')),
                ('cons_c', models.TextField(blank=True, verbose_name='Cons')),
                ('bonus_2w', models.CharField(default='Нет бонусов', max_length=300, verbose_name='Bonuses in short')),
                ('bonus', models.TextField(blank=True, verbose_name='Bonuses')),
                ('accepted_payments', models.TextField(blank=True, verbose_name='Payment processing')),
            ],
            options={
                'ordering': ['rate'],
            },
        ),
    ]
