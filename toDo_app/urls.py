from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('tasks/', views.TacheList.as_view(), 
                    name='tasks-list'),
    path('tasks/<int:pk>/', views.TacheDetail.as_view(), 
                    name='task-details'),
    path('finish/', views.TacheFinishList.as_view(),
                    name='tasks-finish'),
    path('finish/<int:pk>/', views.TacheFinishDetail.as_view(),
                    name='task-finish-detail'),

    path('tasks/for_today/', views.TacheForTodayList.as_view(), 
                    name='tasks-today'),
    path('tasks/for_today/<int:pk>/', views.TacheForTodayDetail.as_view(), 
                    name='task-today'),

    path('tasksVisualisator/', views.TasksVisulisator.as_view(),
         name='tasks-visualisator'),

    path('tasksVisualisator/<int:pk>/', views.TasksVisulisatorDetail.as_view(),
         name='taskDetail-visualisator'),

    path('index/', views.index,
         name="index"),

])
