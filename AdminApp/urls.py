from django.urls import path
from AdminApp.Views import room_view, user_view, workstation_view

urlpatterns=[
    # workstation
    path('workstation/list', workstation_view.getWorkstations, name='workstationList'),
    path('workstation/del/<int:id>', workstation_view.deleteWorkstation, name='workstationDelete'),
    path('workstation/insert', workstation_view.insertWorkstation, name='workstationInsert'),
    path('workstation/modify', workstation_view.modifyWorkstation, name='workstationModify'),
    path('workstation/getInfo', workstation_view.getWorkstationStatus, name='workstationInfo'),
    path('workstation/sanitize', workstation_view.sanizieWorkstation, name='workstationSanitize'),
    path('workstation/failure/del/<int:id>', workstation_view.deleteWorkstationFailure, name='workstationFailureDelete'),
    path('workstation/failure/delall/<int:workid>', workstation_view.deleteWorkstationFailureByWorkstationId, name='workstationFailureDeleteByWorkstationId'),
    path('workstation/failure/insert', workstation_view.insertWorkstationFailure, name='workstationFailureInsert'),
    path('workstation/failure/modify', workstation_view.modifyWorkstationFailure, name='workstationFailureModify'),
    path('workstation/failure/list', workstation_view.getWorkstationsFailure, name='workstationFailureList'),
    #rooms
    path('room/list', room_view.getRooms, name='roomList'),
    path('room/del/<int:id>', room_view.deleteRoom, name='roomDelete'),
    path('room/insert', room_view.insertRoom, name='roomInsert'),
    path('room/modify', room_view.modifyRoom, name='roomModify'),
    path('room/failure/del/<int:id>', room_view.deleteRoomFailure, name='roomFailureDelete'),
    path('room/failure/insert', room_view.insertRoomFailure, name='roomFailureInsert'),
    path('room/failure/modify', room_view.modifyRoomFailure, name='roomFailureModify'),
    path('room/failure/list', room_view.getRoomsFailure, name='roomFailureList'),
    # user
    path('user/list', user_view.getUsers, name='userList'),
    path('user/del/<int:id>', user_view.deleteUser, name='userDelete'),
    path('user/insert', user_view.insertUser, name='userInsert'),
    path('user/modify', user_view.modifyUser, name='userModify'),
    path('user/login', user_view.loginUser, name='login'),
    path('user/bookings/<int:userId>', user_view.userBookings, name='userBookings'),
]