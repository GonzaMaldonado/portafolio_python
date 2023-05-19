from django.urls import path
from .views import TasksView, TasksCompletedView, TaskDetailView, NewTaskView, task_complete, task_delete

app_name = 'tasks'
urlpatterns = [
    path('', TasksView.as_view(), name='home'),
    path('completed/', TasksCompletedView.as_view(), name='completed_tasks'),
    path('new_task/', NewTaskView.as_view(), name='new_task'),
    path('<int:task_id>/', TaskDetailView.as_view(), name='task_detail'),
    path('<int:task_id>/complete/', task_complete, name='task_complete'),
    path('<int:task_id>/delete/', task_delete, name='task_delete'),
]