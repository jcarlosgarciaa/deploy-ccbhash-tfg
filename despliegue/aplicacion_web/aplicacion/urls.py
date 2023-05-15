from django.urls import path

from . import views

urlpatterns = [path('',views.index,name='index'),
                path('ccbhash/', views.ccbhash,name='ccbhash'),
                path('classify_again/', views.classify_again, name='classify_again'),
                path('send_malware/', views.send_malware, name='send_malware')]