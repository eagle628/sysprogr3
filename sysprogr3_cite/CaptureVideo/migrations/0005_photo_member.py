# Generated by Django 2.1.4 on 2018-12-25 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CaptureVideo', '0004_auto_20181217_0135'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='member',
            field=models.CharField(default='', max_length=200),
        ),
    ]
