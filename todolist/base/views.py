from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Imports for Reordering Feature
from django.views import View
from django.db import transaction

from .models import Task
from .forms import PositionForm
from datetime import date, timedelta

class DashboardView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'dashboard'
    template_name = 'base/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today_tasks = Task.objects.filter(user=user, due_date=date.today())[:3]
        week_start = date.today() - timedelta(days=date.today().weekday())
        week_completed_tasks = Task.objects.filter(user=user, completed=True, due_date__gte=week_start)
        today_completed_tasks = Task.objects.filter(user=user, completed=True, due_date=date.today())[:3]

        context['today_tasks'] = today_tasks
        context['week_completed_tasks'] = week_completed_tasks
        context['today_completed_tasks'] = today_completed_tasks

        return context

    def get_queryset(self):
        # This method is required by ListView, but we don't actually use it for fetching tasks
        return Task.objects.none()

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    

class TaskListWorkView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'work'
    template_name = 'base/task_list_work.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['work'] = context['work'].filter(user=self.request.user)
        context['count'] = context['work'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['work'] = context['work'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context 
    
class TaskCreateWorkView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'complete']
    template_name = 'base/task_form.html'  # You need to create this template
    success_url = reverse_lazy('work')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateWorkView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'complete']
    template_name = 'base/task_form.html'  # You need to create this template
    success_url = reverse_lazy('work')


class TaskDeleteWorkView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task_confirm_delete.html'  # You need to create this template
    success_url = reverse_lazy('work')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class WorkTaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('school'))

class TaskListShoppingView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'shopping'
    template_name = 'base/task_list_shopping.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shopping'] = context['shopping'].filter(user=self.request.user)
        context['count'] = context['shopping'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['shopping'] = context['shopping'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context

class TaskListEventView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'event'
    template_name = 'base/task_list_event.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = context['event'].filter(user=self.request.user)
        context['count'] = context['event'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['event'] = context['event'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('main')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('school')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('school')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

class Dashboard(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'school'
    template_name = 'base/dashboard.html'
    

class SchoolTaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'school'
    template_name = 'base/task_list_school.html'

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = context['school'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['school'] = context['school'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context
    

class SchoolTaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'complete' ]
    success_url = reverse_lazy('school')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SchoolTaskCreate, self).form_valid(form)


class SchoolTaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'complete']
    success_url = reverse_lazy('school')

class SchoolDeleteView(DeleteView, LoginRequiredMixin):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('school')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class SchoolTaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('school'))
