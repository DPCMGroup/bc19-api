from django.urls import path
from AdminApp import views

urlpatterns=[
    # workstation
    path('workstation/list', views.getWorkstations, name='worstationList'),
    path('workstation/del/<int:id>', views.deleteWorkstation, name='workstationDelete'),
    path('workstation/insert', views.insertWorkstation, name='workstationInsert'),
    path('workstation/modify', views.modifyWorkstation, name='workstationModify'),
    path('workstation/getInfo', views.getWorkstationStatus, name='workstationInfo'),
    path('workstation/sanitize', views.sanizieWorkstation, name='workstationSanitize'),
    #rooms
    path('room/list', views.getRooms, name='roomList'),
    path('room/del/<int:id>', views.deleteRoom, name='roomDelete'),
    path('room/insert', views.insertRoom, name='roomInsert'),
    path('room/modify', views.modifyRoom, name='roomModify'),
    # user
    path('user/list', views.getUsers, name='userList'),
    path('user/del/<int:id>', views.deleteUser, name='userDelete'),
    path('user/insert', views.insertUser, name='userInsert'),
    path('user/modify', views.modifyUser, name='userModify'),
    path('user/login', views.loginUser, name='login'),
    path('user/bookings/<int:userId>', views.userBookings, name='userBookings'),
]