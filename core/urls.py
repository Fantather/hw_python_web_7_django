from django.urls import path

from core import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name="task_list"),
    path('add/', views.TaskCreateView.as_view(), name="task_create"),
    path('delete/<int:task_id>/', views.TaskDeleteView.as_view(), name="task_delete"),
]
