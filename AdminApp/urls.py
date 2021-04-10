from django.urls import path, include
from AdminApp import views

urlpatterns=[
    # workstation
    path('workstation/list', views.getWorkstations, name='list'),
    path('workstation/del/<int:id>', views.deleteWorkstation, name='delete'),
    path('workstation/insert', views.insertWorkstation, name='insert'),
    path('workstation/getInfo', views.getWorkstationStatus, name='getWorkstationInfo'),
    # user
    path('user/login', views.loginUser, name='login'),
    path('user/bookings/<int:userId>', views.userBookings, name='userBookings'),
]