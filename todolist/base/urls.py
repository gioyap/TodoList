from django.urls import path
from .views import (
    SchoolDeleteView, Dashboard, SchoolTaskList,
    TaskCreateWorkView, TaskUpdateWorkView, TaskDeleteWorkView,
    SchoolTaskCreate, SchoolTaskReorder, SchoolTaskUpdate, TaskDetail,
    CustomLoginView, RegisterPage, TaskListWorkView, TaskListShoppingView, TaskListEventView,
    WorkTaskReorder
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('', Dashboard.as_view(), name='main'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('work/', TaskListWorkView.as_view(), name='work'),
    path('shopping/', TaskListShoppingView.as_view(), name='shopping'),
    path('event/', TaskListEventView.as_view(), name='event'),

    path('school/', SchoolTaskList.as_view(), name='school'),
    path('task-create/', SchoolTaskCreate.as_view(), name='school-create'),
    path('task-update/<int:pk>/', SchoolTaskUpdate.as_view(), name='school-update'),
    path('task-delete/<int:pk>/', SchoolDeleteView.as_view(), name='school-delete'),
    path('task-reorder/', SchoolTaskReorder.as_view(), name='school-reorder'),

    path('work/', TaskListWorkView.as_view(), name='work'),
    path('work-create/', TaskCreateWorkView.as_view(), name='work-create'),
    path('work-update/<int:pk>/', TaskUpdateWorkView.as_view(), name='work-update'),
    path('work-delete/<int:pk>/', TaskDeleteWorkView.as_view(), name='work-delete'),
    path('task-reorder/', WorkTaskReorder.as_view(), name='work-reorder'),
]
