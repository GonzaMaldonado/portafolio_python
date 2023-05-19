from django.views.generic import ListView, UpdateView, CreateView
from .models import Task
from .forms import TaskForm
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class TasksView(ListView):
    model = Task
    template_name = 'tasks/home.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user, completed__isnull=True).order_by('-important')
        return queryset

@method_decorator(login_required, name='dispatch')
class TasksCompletedView(ListView):
    model = Task
    template_name = 'tasks/home.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user, completed__isnull=False)
        return queryset

@method_decorator(login_required, name='dispatch')
class TaskDetailView(UpdateView):
    model = Task
    template_name = 'tasks/task_detail.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks:home')

    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs['task_id'], user=self.request.user)

@method_decorator(login_required, name='dispatch')
class NewTaskView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/new_task.html'
    success_url = reverse_lazy('tasks:home')

    def form_valid(self, form):
        new_task = form.save(commit=False)
        new_task.user = self.request.user
        new_task.save()
        return super().form_valid(form)
    

@login_required
def task_complete(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        task.completed = timezone.now()
        task.save()
        return redirect('tasks:home')

@login_required
def task_delete(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        task.delete()
        return redirect('tasks:home')