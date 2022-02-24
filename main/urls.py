from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index,name='base url'),
    path('<int:id>',views.specific,name='each user url'),
    #path('add',views.add_data,name='database'),
]
