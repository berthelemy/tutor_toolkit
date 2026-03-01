from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.day_view, name='day'),
    path('week/', views.week_view, name='week'),
    path('student/', views.student_view, name='student'),
]
