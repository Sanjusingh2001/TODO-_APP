from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/todos/', views.todo_list_api, name='todo_list_api'),
    path('api/todos/<int:todo_id>/', views.todo_detail_api, name='todo_detail_api'),
]