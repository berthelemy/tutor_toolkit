from django.urls import path

from . import views

app_name = 'schools'

urlpatterns = [
    path('switch/', views.switch_school, name='switch'),
]
