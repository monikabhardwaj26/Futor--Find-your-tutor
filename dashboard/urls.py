from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('student/', views.student_dashboard, name='student'),
    path('teacher/', views.teacher_dashboard, name='teacher'),
    path('favorite/<int:teacher_id>/', views.toggle_favorite, name='toggle_favorite'),
]
