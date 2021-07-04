from django.urls import path
from personal_app.views import LoginView, UserView, GroupView

urlpatterns = [
    path('v1/login/', LoginView.as_view()),
    path('v1/user/', UserView.as_view()),
    path('v1/group/', GroupView.as_view()),
]
