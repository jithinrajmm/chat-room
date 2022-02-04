from django.urls import path 
from base import views
from django.contrib.auth import logout


urlpatterns = [

    path('login',views.loginPage,name='login'),
    path('logout',views.logoutPage,name='logout'),
    path('register',views.registerPage,name='register'),
    path('namecheck',views.namecheck,name='namecheck'),
    path('profile/<int:pk>',views.userProfile,name = "profile"),
    path('update_user',views.update_user,name='update_user'),

    # mobile responsive
    path('topic',views.topics,name='topic'),
    path('activity',views.activity,name= 'activity'),

    path('delete_message/<int:pk>',views.delete_message,name='delete_message'),


    path('',views.home,name='home'),
    path('roomDetail/<str:pk>',views.singleRoom,name= "roomDetail"),

    path('create_room',views.createRoom,name='create_room'),
    path('update_room/<int:pk>',views.updateRoom,name='update_room'),
    path('delete_room/<int:pk>',views.deleteRoom,name = "delete_room")
]
