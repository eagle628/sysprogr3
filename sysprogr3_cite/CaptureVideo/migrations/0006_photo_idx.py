# Generated by Django 2.1.4 on 2018-12-26 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CaptureVideo', '0005_photo_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='idx',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
