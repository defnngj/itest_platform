from django.urls import path
from app_case import views


urlpatterns = [
    path('', views.list_case),
    path('send_req/', views.send_req),
]
