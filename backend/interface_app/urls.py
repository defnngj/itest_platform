from django.urls import path
from interface_app.views import ProjectView
from interface_app.views import ModuleView

urlpatterns = [
    path('v1/project/<int:pk>/', ProjectView.as_view()),
    path('v1/project/', ProjectView.as_view()),
    path('v1/module/<int:pk>/', ModuleView.as_view()),
    path('v1/module/', ModuleView.as_view()),
]
