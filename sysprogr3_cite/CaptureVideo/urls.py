from django.urls import path

from . import views

app_name = 'CaptureVideo'
urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('SendImageForm/', views.SendImageForm.as_view(), name='sendimageform'),
    #path('processing/', views.processing, name='processing'),
    path('Processing/', views.StartProcessing.as_view(), name='processing'),
    #path('processing/progress/<int:pk>/', views.progress, name='progress'),
]
