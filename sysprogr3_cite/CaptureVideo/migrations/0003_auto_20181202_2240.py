# Generated by Django 2.1.3 on 2018-12-02 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CaptureVideo', '0002_progress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='CaptureVideo/media', verbose_name='input'),
        ),
    ]
