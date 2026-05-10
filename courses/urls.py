from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.courses_view, name='courses'),
    path('get-subjects/', views.get_subjects_ajax, name='get_subjects'),
]
