import os
import re
import time
import uuid
from multiprocessing import Process

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import generic, View
from .forms import PhotoForm, PassForm
from .models import Photo, Progress

#from background_task import background
import cv2
import numpy as np
import logging

def index(request):
    if request.method == 'GET':
        image_set = Photo.objects.all()
        image_set.delete()
        return render(request, 'CaptureVideo/index.html')
    elif request.method == 'POST':
        return redirect('CaptureVideo:sendimageform')

class SendImageForm(View):
    template_name = 'CaptureVideo/sendimageform.html'
    mode = False
    image_name_list = []

    def get(self, request):
        form1 = PhotoForm()
        form2 = PassForm()
        return render(request, self.template_name, {'form1': form1, 'form2':form2, 'mode':self.mode},)

    def post(self, request, *args):
        if 'upload' in request.POST:
            form = PhotoForm(self.request.POST, self.request.FILES)
            if not form.is_valid():
                raise ValueError('invalid form')

            photo = Photo()
            photo.image = form.cleaned_data['image']
            photo.stage = 'input'
            photo.save()
            self.image_name_list.append(photo.image.name)
            logging.debug('upload to : '+photo.image.name)
            self.mode = True
            return self.get(request)
        elif 'next' in request.POST:
            return redirect('CaptureVideo:processing')

class StartProcessing(View):
    template_name = 'CaptureVideo/processing.html'

    def get(self, request, *args):
        return render(request, self.template_name)

    def post(self, request):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        images = Photo.objects.filter(stage='input')
        logging.debug(len(images))
        for image in images:
            photo = Photo()
            path = ImageTranspose(os.path.join(BASE_DIR,'media'), image.image.name)
            photo.image = path
            photo.stage = 'output'
            photo.save()
        return redirect('CaptureVideo:test')


def test(request):
    if request.method == 'GET':
        input_images = Photo.objects.all().filter(stage='input')
        output_images = Photo.objects.all().filter(stage='output')
        return render(request,'CaptureVideo/test.html',{'Input':input_images, 'Output':output_images})
    elif request.method == 'POST':
        # media clean
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        image_set = Photo.objects.all()
        for image in image_set :
            logging.debug(image.image.url)
            os.remove(os.path.join(BASE_DIR,'media',image.image.name))
        return redirect('http://google.com/')

####################### Local function

def search_img_name(image_root, extension):
    image_name = []
    files = os.listdir(image_root)
    for file in files:
        index = re.search(extension, file)# 拡張子が，jpgのものを検出
        if index:
            image_name.append(file)
    return image_name

def ImageTranspose(image_root, image_name):
    # 入力画像をグレースケールで読み込み
    gray = cv2.imread(os.path.join(image_root,image_name), 0)
    # 方法3
    dst3 = cv2.Laplacian(gray, cv2.CV_32F, ksize=7)
    # 結果を出力
    name = str(uuid.uuid4()).replace('-', '')
    output_path =os.path.join(image_root,'CaptureVideo','media',name+'.jpg')
    cv2.imwrite(output_path, dst3)
    return output_path
###############################################################################


"""
def sendimageform(request):
    if request.method == 'GET':
        return render(request, 'CaptureVideo/sendimageform.html', {
            'form': PhotoForm(),
        })
    elif request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if not form.is_valid():
            raise ValueError('invalid form')

        photo = Photo()
        photo.image = form.cleaned_data['image']
        photo.save()
        logger.debug('save model')
            #if 'upload' in request.POST:
        if 'upload' in request.POST:
            #return self.get(request)
            return redirect('CaptureVideo:test')
        elif 'next' in request.POST:
            return redirect('CaptureVideo:test')

def processing(request):
    if request.method == 'GET':
        return render(request, 'CaptureVideo/processing.html')
    elif request.method == 'POST':
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        image_root = os.path.join(BASE_DIR,'media','CaptureVideo','media')
        image_name_set = search_img_name(image_root, '.png')
        for image_name in image_name_set :
            os.remove(os.path.join(image_root,image_name))
        some_long_duration_process(1,2)
        return redirect('CaptureVideo:test')

@background(queue='queue_name1', schedule=2)
def some_long_duration_process(some_param1, some_param2):
    # back ground Process
    for i in range(1, 11):
        time.sleep(some_param1)
        k = i * some_param2  # 初回に10、次に20...最後は100が入る。進捗のパーセントに対応

def progress(request, pk):
    context = {
        'progress': get_object_or_404(Progress, pk=pk)
    }
    return render(request, 'CaptureVideo/progress.html', context)

"""
