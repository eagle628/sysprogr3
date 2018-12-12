from django.db import models

class Photo(models.Model):
    image = models.ImageField(
        upload_to='CaptureVideo/media',
        verbose_name='input',
        )

class Progress(models.Model):
    """Progress Model"""
    num = models.IntegerField('Progress', default=0)
    def __str__(self):
        return self.num
