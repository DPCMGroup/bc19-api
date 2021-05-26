from django.urls import path
from AdminApp.Views import room_view, user_view, workstation_view, booking_view

urlpatterns = [
    # workstation
    path('workstation/list', workstation_view.getWorkstations, name='workstationList'),
    path('workstation/del/<int:id>', workstation_view.deleteWorkstation, name='workstationDelete'),
    path('workstation/insert', workstation_view.insertWorkstation, name='workstationInsert'),
    path('workstation/modify', workstation_view.modifyWorkstation, name='workstationModify'),
    path('workstation/getInfo', workstation_view.getWorkstationStatus, name='workstationInfo'),
    path('workstation/sanitize', workstation_view.sanizieWorkstation, name='workstationSanitize'),
    path('workstation/dirty/list', workstation_view.workstationToSanitize, name='workstationToSanitize'),
    # rooms
    path('room/list', room_view.getRooms, name='roomList'),
    path('room/del/<int:id>', room_view.deleteRoom, name='roomDelete'),
    path('room/insert', room_view.insertRoom, name='roomInsert'),
    path('room/modify', room_view.modifyRoom, name='roomModify'),
    path('room/dirty/list', room_view.roomToSanitize, name='roomToSanitize'),
    # user
    path('user/list', user_view.getUsers, name='userList'),
    path('user/del/<int:id>', user_view.deleteUser, name='userDelete'),
    path('user/insert', user_view.insertUser, name='userInsert'),
    path('user/modify', user_view.modifyUser, name='userModify'),
    path('user/login', user_view.loginUser, name='login'),
    path('user/bookings/<int:userId>', user_view.userBookings, name='userBookings'),
    # bookings
    path('booking/insert', booking_view.insertBooking, name='bookingInsert'),
    path('booking/list', booking_view.getBookings, name='bookingList'),
    path('booking/modify', booking_view.modifyBooking, name='bookingModify'),
    path('booking/del/<int:id>', booking_view.deleteBooking, name='bookingDelete'),
]
