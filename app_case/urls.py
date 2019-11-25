from django.urls import path
from app_case import views


urlpatterns = [
    path('', views.list_case),
    path('send_req/', views.send_req),
    path('assert_result/', views.assert_result),
    path('get_select_data/', views.get_select_data),
    path('save_case/', views.save_case),
]
