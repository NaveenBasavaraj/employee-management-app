from django.urls import path
from . import views

urlpatterns = [
    path('', views.poll_list, name='poll_list'),
    path('<int:pk>/', views.poll_detail, name='poll_detail'),
    path('create/', views.poll_create, name='poll_create'),
    path('choice/create/', views.choice_create, name='choice_create'),
]
