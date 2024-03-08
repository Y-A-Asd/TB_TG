from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_conversation, name='start_conversation'),
    path('<int:convo_id>/', views.get_conversation, name='get_conversation'),
    path('', views.conversations, name='conversations')
]
