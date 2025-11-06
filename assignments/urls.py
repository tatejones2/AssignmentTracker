"""
URL configuration for assignments app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Assignment URLs
    path('', views.assignment_list, name='assignment_list'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('create/', views.assignment_create, name='assignment_create'),
    path('<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('<int:pk>/update/', views.assignment_update, name='assignment_update'),
    path('<int:pk>/delete/', views.assignment_delete, name='assignment_delete'),
    
    # Course URLs
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/<int:pk>/update/', views.course_update, name='course_update'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),
]
