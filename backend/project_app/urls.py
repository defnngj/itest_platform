from django.urls import path
from project_app.views import ProjectView, ProjectsView

urlpatterns = [
    path('v1/project/<int:pk>/', ProjectView.as_view()),
    path('v1/projects/', ProjectsView.as_view()),
]
