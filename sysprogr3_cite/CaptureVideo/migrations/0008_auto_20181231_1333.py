# Generated by Django 2.1.4 on 2018-12-31 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CaptureVideo', '0007_photo_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='result',
            field=models.BinaryField(null=True),
        ),
    ]
