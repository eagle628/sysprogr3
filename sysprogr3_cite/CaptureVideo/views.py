import os
import re
import time
import uuid
from multiprocessing import Process

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import generic, View
from .forms import PhotoForm, PassForm
from .models import Photo, Progress

from . import ML_func

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
        if not request.session.session_key:
            request.session.create()
        logging.debug('Session ID : '+request.session.session_key)
        if 'idx' not in request.session:
            request.session['idx'] = 0
        return redirect('CaptureVideo:sendimageform')

class SendImageForm(View):
    template_name = 'CaptureVideo/sendimageform.html'
    mode = False
    image_name_list = []

    def get(self, request):
        form1 = PhotoForm()
        form2 = PassForm()
        logging.debug('Session ID : '+request.session.session_key)
        return render(request, self.template_name, {'form1': form1, 'form2':form2, 'mode':self.mode},)

    def post(self, request, *args):
        if 'upload' in request.POST:
            form = PhotoForm(self.request.POST, self.request.FILES)
            if not form.is_valid():
                raise ValueError('invalid form')

            photo = Photo()
            photo.image = form.cleaned_data['image']
            photo.stage = 'input'
            photo.member = request.session.session_key
            photo.idx = request.session['idx']
            photo.save()
            self.image_name_list.append(photo.image.name)
            logging.debug('Session ID : '+photo.member)
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
        ID = request.session.session_key
        logging.debug('Session ID : '+ID)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        images = Photo.objects.filter(stage='input',member=ID,idx=request.session['idx'])
        for image in images:
            path_set = ML_func.preprocess(os.path.join(BASE_DIR,'media'), image.image.name, crop_size = 28)
            logging.debug(path_set)
            for path in path_set:
                photo = Photo()
                photo.image = path
                photo.stage = 'output'
                photo.member = ID
                photo.idx = request.session['idx']
                photo.result = ML_func.est_locale(path)
                photo.save()
        return redirect('CaptureVideo:result')


class Result(View):
    template_name = 'CaptureVideo/result.html'

    def get(self, request, *args):
        ID = request.session.session_key
        input_images = Photo.objects.filter(stage='input',member=ID,idx=request.session['idx'])
        output_images = Photo.objects.filter(stage='output',member=ID,idx=request.session['idx'])
        for output in output_images :
            logging.debug(np.frombuffer(output.result, dtype=np.float32))
        return render(request,'CaptureVideo/result.html',{'Input':input_images, 'Output':output_images})

    def post(self, request):
        ID = request.session.session_key
        if 'complete' in request.POST:
            # media clean
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            image_set = Photo.objects.filter(member=ID)
            for image in image_set :
                logging.debug(image.image.url)
                os.remove(os.path.join(BASE_DIR,'media',image.image.name))
            image_set.delete()
            return redirect('https://portal.nap.gsic.titech.ac.jp/portal.pl?GASF=CERTIFICATE,IG.GRID,IG.OTP&GAREASONCODE=-1&GARESOURCEID=resourcelistID2&GAURI=https://portal.nap.gsic.titech.ac.jp/GetAccess/ResourceList&Reason=-1&APPID=resourcelistID2&URI=https://portal.nap.gsic.titech.ac.jp/GetAccess/ResourceList')
        elif 'again' in request.POST:
            request.session['idx'] = request.session['idx'] + 1
            return redirect('CaptureVideo:sendimageform')


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
