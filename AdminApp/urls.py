from django.urls import path, include
from AdminApp import views

urlpatterns=[
    path('workstation/list', views.getWorkstations, name='list'),
    path('workstation/<int:id>', views.deleteWorkstation, name='delete'),
    path('workstation/insert', views.insertWorkstation, name='insert')
]