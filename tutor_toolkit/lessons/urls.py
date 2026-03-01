from django.urls import path

from . import views

app_name = 'lessons'

urlpatterns = [
    path('', views.LessonListView.as_view(), name='list'),
    path('new/', views.LessonCreateView.as_view(), name='create'),
    path('<int:pk>/', views.LessonDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.LessonUpdateView.as_view(), name='edit'),
    path('<int:lesson_id>/objectives/new/', views.LessonObjectiveCreateView.as_view(), name='objective_create'),
    path('<int:lesson_id>/resources/new/', views.LessonResourceCreateView.as_view(), name='resource_create'),
    path('<int:lesson_id>/homework/new/', views.HomeworkTaskCreateView.as_view(), name='homework_create'),
    path('<int:lesson_id>/notes/new/', views.LessonNoteCreateView.as_view(), name='note_create'),
]
