from django.urls import path, include

import views

app_name = 'chat'
urlpatterns = [
    path('chats/', views.chats, name='chats'),
    path('chat/<str:room>/', views.room, name='room'),
]
