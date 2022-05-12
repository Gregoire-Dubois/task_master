from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('tasks/', views.TacheList.as_view(), 
                    name='tasks-list'),
    path('tasks/<int:pk>/', views.TacheDetail.as_view(), 
                    name='task-details'),
    path('users/', views.UsersList.as_view(), 
                    name='users-list'),
    path('users/<int:pk>/', views.UserDetails.as_view(), 
                    name='user-details'),
    path('tasks/for_today/', views.TacheForTodayList.as_view(), 
                    name='tasks-today'),
    path('tasks/for_today/<int:pk>/', views.TacheForTodayDetail.as_view(), 
                    name='task-today'),

])


