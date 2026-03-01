from django.urls import path

from . import views

app_name = 'lessons'

urlpatterns = [
    path('', views.LessonListView.as_view(), name='list'),
    path('new/', views.LessonCreateView.as_view(), name='create'),
    path('<int:pk>/', views.LessonDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.LessonUpdateView.as_view(), name='edit'),
    path('<int:lesson_id>/objectives/new/', views.LessonObjectiveCreateView.as_view(), name='objective_create'),
    path('objectives/<int:pk>/edit/', views.LessonObjectiveUpdateView.as_view(), name='objective_edit'),
    path('objectives/<int:pk>/delete/', views.LessonObjectiveDeleteView.as_view(), name='objective_delete'),
    path('<int:lesson_id>/resources/new/', views.LessonResourceCreateView.as_view(), name='resource_create'),
    path('resources/<int:pk>/edit/', views.LessonResourceUpdateView.as_view(), name='resource_edit'),
    path('resources/<int:pk>/delete/', views.LessonResourceDeleteView.as_view(), name='resource_delete'),
    path('<int:lesson_id>/homework/new/', views.HomeworkTaskCreateView.as_view(), name='homework_create'),
    path('homework/<int:pk>/edit/', views.HomeworkTaskUpdateView.as_view(), name='homework_edit'),
    path('homework/<int:pk>/delete/', views.HomeworkTaskDeleteView.as_view(), name='homework_delete'),
    path('<int:lesson_id>/notes/new/', views.LessonNoteCreateView.as_view(), name='note_create'),
    path('notes/<int:pk>/edit/', views.LessonNoteUpdateView.as_view(), name='note_edit'),
    path('notes/<int:pk>/delete/', views.LessonNoteDeleteView.as_view(), name='note_delete'),
]
