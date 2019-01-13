from django.urls import path

from . import views

app_name = 'CaptureVideo'
urlpatterns = [
    path('', views.index, name='index'),
    path('Result/', views.Result.as_view(), name='result'),
    path('SendImageForm/', views.SendImageForm.as_view(), name='sendimageform'),
    path('Processing/', views.StartProcessing.as_view(), name='processing'),
    path('Tree/', views.Tree.as_view(), name='tree'),
]
