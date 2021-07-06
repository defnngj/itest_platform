from django.urls import path
from interface_app.views import ProjectView, ProjectsView
from interface_app.views import ModuleView, ModulesView

urlpatterns = [
    path('v1/project/<int:pk>/', ProjectView.as_view()),
    path('v1/projects/', ProjectsView.as_view()),
    path('v1/module/<int:pk>/', ModuleView.as_view()),
    path('v1/modules/', ModulesView.as_view()),
]
