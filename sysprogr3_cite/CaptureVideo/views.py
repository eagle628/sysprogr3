import os
import re
import time
import uuid
from multiprocessing import Process

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import generic, View
from .forms import PhotoForm, PassForm, SerachForm, ConfirmForm, MapForm
from .models import Photo, Progress

from .CV_Module import ML_func, SearchDirection, colormap, treemap

import chainer.functions as F

#from background_task import background
import cv2
import numpy as np
import logging

def index(request):
    if request.method == 'GET':
        image_set = Photo.objects.all()
        image_set.delete()
        return render(request, 'CaptureVideo/index.html',{'Form':MapForm()})
    elif request.method == 'POST':
        if not request.session.session_key:
            request.session.create()
        logging.debug('Session ID : '+request.session.session_key)
        if 'idx' not in request.session:
            request.session['idx'] = 0
        request.session['map'] = request.POST['map']
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
            path_set = ML_func.preprocess(os.path.join(BASE_DIR,'media'), image.image.name, crop_size = 1000)
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
        input_images = Photo.objects.filter(stage='input',member=ID)
        output_images = Photo.objects.filter(stage='output',member=ID)
        Flag = False
        for output in output_images :
            if Flag is False :
                result = np.array([np.frombuffer(output.result, dtype=np.float32)])
                Flag = True
            else :
                result += np.array([np.frombuffer(output.result, dtype=np.float32)])
        logging.debug('result : ')
        logging.debug(result)
        result = F.softmax(result).data
        # make heatmap
        logging.debug('Softmax result : ')
        logging.debug(result)
        tmp = np.max(result)
        result = (result*200/tmp).astype(np.int64)
        result = result.tolist()[0]
        #result = [200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,]
        logging.debug('nomarilize :')
        logging.debug(result)
        #result = (result).tolist()[0]
        #logging.debug(result)
        #result = (200*np.random.rand(1,52)).tolist()[0] # test
        path = os.path.dirname(os.path.abspath(__file__))
        MEDIA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'media','CaptureVideo','media')

        logging.debug('make HeatMap FB1')
        FB1 = colormap.Heatmapimage(os.path.join(path,'CV_Module','Map_Honkan','bf_all.jpg'), quality=1)
        for itr in range(39,51) :
            FB1.add_circle(itr, result[itr])
        photo = Photo()
        photo.image = FB1.export_heatmap_with_colorbar(MEDIA_DIR)
        photo.stage = 'HeatMap'
        photo.member = ID
        photo.idx = request.session['idx']
        photo.save()

        logging.debug('make HeatMap F1')
        F1 = colormap.Heatmapimage(os.path.join(path,'CV_Module','Map_Honkan','1f_all.jpg'), quality=1)
        for itr in range(0,12) :
            F1.add_circle(itr, result[itr])
        photo = Photo()
        photo.image = F1.export_heatmap_with_colorbar(MEDIA_DIR)
        photo.stage = 'HeatMap'
        photo.member = ID
        photo.idx = request.session['idx']
        photo.save()

        logging.debug('make HeatMap F2')
        F2 = colormap.Heatmapimage(os.path.join(path,'CV_Module','Map_Honkan','2f_all.jpg'), quality=1)
        for itr in range(13,25) :
            F2.add_circle(itr, result[itr])
        photo = Photo()
        photo.image = F2.export_heatmap_with_colorbar(MEDIA_DIR)
        photo.stage = 'HeatMap'
        photo.member = ID
        photo.idx = request.session['idx']
        photo.save()

        logging.debug('make HeatMap F3')
        F3 = colormap.Heatmapimage(os.path.join(path,'CV_Module','Map_Honkan','3f_all.jpg'), quality=1)
        for itr in range(26,38) :
            F3.add_circle(itr, result[itr])
        photo = Photo()
        photo.image = F3.export_heatmap_with_colorbar(MEDIA_DIR)
        photo.stage = 'HeatMap'
        photo.member = ID
        photo.idx = request.session['idx']
        photo.save()

        # Result Heatmap
        heatmap_images = Photo.objects.filter(stage='HeatMap',member=ID,idx=request.session['idx'])

        return render(request,self.template_name,{'Input':input_images, 'Output':output_images, 'Result':heatmap_images, 'Form':SerachForm()})

    def post(self, request, *args):
        ID = request.session.session_key
        if 'complete' in request.POST:
            form = SerachForm(self.request.POST)
            if not form.is_valid():
                raise ValueError('invalid form')
                return redirect('CaptureVideo:result')
            #start = form.cleaned_data['start']
            start_idx = request.POST['start']
            end_idx = request.POST['end']
            logging.debug('start point : ' + start_idx)
            logging.debug('end point : ' + end_idx)
            request.session['start_idx'] = int(start_idx)
            request.session['end_idx'] = int(end_idx)
            return redirect('CaptureVideo:tree')
        elif 'again' in request.POST:
            request.session['idx'] = request.session['idx'] + 1
            return redirect('CaptureVideo:sendimageform')

class Tree(View):
    template_name = 'CaptureVideo/tree.html'

    def get(self, request, *args):
        # Internal function
        def extract_node_list(node_list, st, en):
            li = []
            for node in node_list:
                if node >= st and node <=en:
                    li.append(node)
            return li
        # main
        ID = request.session.session_key
        tree = SearchDirection.search_tree(request.session['start_idx'], request.session['end_idx'])
        # set path
        path = os.path.dirname(os.path.abspath(__file__))
        MEDIA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'media','CaptureVideo','media')

        logging.debug('make TreeMap FB1')
        FB1 = treemap.Treemapimage(os.path.join(path,'CV_Module','Map_Honkan','bf_all.jpg'), quality=1)
        photo = Photo()
        photo.image = FB1.export_treemap(MEDIA_DIR, extract_node_list(tree, 0, 12))
        photo.stage = 'TreeMap'
        photo.member = ID
        photo.idx = request.session['idx']
        photo.save()

        logging.debug('make TreeMap F1')
        F1 = treemap.Treemapimage(os.path.join(path,'CV_Module','Map_Honkan','bf_all.jpg'), quality=1)
        photo = Photo()
        photo.image = F1.export_treemap(MEDIA_DIR, extract_node_list(tree, 13, 25))
        photo.stage = 'TreeMap'
        photo.member = ID
        photo.idx = request.session['idx']
        photo.save()

        logging.debug('make TreeMap F2')
        F2 = treemap.Treemapimage(os.path.join(path,'CV_Module','Map_Honkan','bf_all.jpg'), quality=1)
        photo = Photo()
        photo.image = F2.export_treemap(MEDIA_DIR, extract_node_list(tree, 26, 38))
        photo.stage = 'TreeMap'
        photo.member = ID
        photo.idx = request.session['idx']
        photo.save()

        logging.debug('make TreeMap F3')
        F3 = treemap.Treemapimage(os.path.join(path,'CV_Module','Map_Honkan','bf_all.jpg'), quality=1)
        photo = Photo()
        photo.image = F3.export_treemap(MEDIA_DIR, extract_node_list(tree, 39, 51))
        photo.stage = 'TreeMap'
        photo.member = ID
        photo.idx = request.session['idx']
        photo.save()

        # Result Treemap
        treemap_images = Photo.objects.filter(stage='TreeMap',member=ID,idx=request.session['idx'])

        return render(request,self.template_name,{'Tree':treemap_images})

    def post(self, request):
        ID = request.session.session_key
        if 'next' in request.POST:
            return redirect('CaptureVideo:confirm')

class Confirm(View):
    template_name = 'CaptureVideo/confirm.html'

    def get(self, request, *args):
        logging.debug(type(request.session['start_idx']))
        return render(request,self.template_name,{'Confirm':ConfirmForm(initial={'answer': 0})})

    def post(self, request):
        ID = request.session.session_key
        if 'complete' in request.POST:
            logging.debug(request.POST['answer'])
            if request.POST['answer'] == '1':
                logging.debug('Save Correct data')
            elif request.POST['answer'] == '0':
                logging.debug('Delete Incorrect data')
            # media clean
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            image_set = Photo.objects.filter(member=ID)
            for image in image_set :
                logging.debug(image.image.url)
                os.remove(os.path.join(BASE_DIR,'media',image.image.name))
            image_set.delete()
            return redirect('https://portal.nap.gsic.titech.ac.jp/portal.pl?GASF=CERTIFICATE,IG.GRID,IG.OTP&GAREASONCODE=-1&GARESOURCEID=resourcelistID2&GAURI=https://portal.nap.gsic.titech.ac.jp/GetAccess/ResourceList&Reason=-1&APPID=resourcelistID2&URI=https://portal.nap.gsic.titech.ac.jp/GetAccess/ResourceList')
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
