from django.urls import path

from . import views

app_name = 'students'

urlpatterns = [
    path('', views.StudentListView.as_view(), name='list'),
    path('new/', views.StudentCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.StudentUpdateView.as_view(), name='edit'),
    path('groups/', views.GroupListView.as_view(), name='groups'),
    path('groups/new/', views.GroupCreateView.as_view(), name='group_create'),
    path('groups/<int:pk>/edit/', views.GroupUpdateView.as_view(), name='group_edit'),
]
