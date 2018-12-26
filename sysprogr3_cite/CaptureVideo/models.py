from django.db import models
import uuid
import os

def get_image_path(self, filename):
    """カスタマイズした画像パスを取得する.

    :param self: インスタンス (models.Model)
    :param filename: 元ファイル名
    :return: カスタマイズしたファイル名を含む画像パス
    """
    prefix = r'CaptureVideo/media/'
    name = str(uuid.uuid4()).replace('-', '')
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension

def delete_previous_file(function):
    """不要となる古いファイルを削除する為のデコレータ実装.

    :param function: メイン関数
    :return: wrapper
    """
    def wrapper(*args, **kwargs):
        """Wrapper 関数.

        :param args: 任意の引数
        :param kwargs: 任意のキーワード引数
        :return: メイン関数実行結果
        """
        self = args[0]

        # 保存前のファイル名を取得
        result = Photo.objects.filter(pk=self.pk)
        previous = result[0] if len(result) else None
        super(Photo, self).save()

        # 関数実行
        result = function(*args, **kwargs)

        # 保存前のファイルがあったら削除
        if previous:
            os.remove(MEDIA_ROOT + '/' + previous.image.name)
        return result
    return wrapper

class Photo(models.Model):
    @delete_previous_file
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Photo, self).save()

    @delete_previous_file
    def delete(self, using=None, keep_parents=False):
        super(Photo, self).delete()

    image = models.ImageField(upload_to=get_image_path)
    stage = models.CharField(max_length=200, default='')
    member = models.CharField(max_length=200, default='')

class Progress(models.Model):
    """Progress Model"""
    num = models.IntegerField('Progress', default=0)
    def __str__(self):
        return self.num
