# Generated by Django 4.2.5 on 2023-11-04 08:53

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=7, samples=None, verbose_name='Цвет'),
        ),
    ]
