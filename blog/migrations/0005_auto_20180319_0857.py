# Generated by Django 2.0.3 on 2018-03-19 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20180315_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Slug'),
        ),
    ]
