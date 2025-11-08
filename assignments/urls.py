"""
URL configuration for assignments app.
"""
from django.urls import path
from . import views
from .views_auth import account_view, account_edit
from .views_learn import (
    learn_hub, podcast_create, podcast_generate, 
    podcast_detail, podcast_download, podcast_delete
)

urlpatterns = [
    # Assignment URLs
    path('', views.assignment_list, name='assignment_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('create/', views.assignment_create, name='assignment_create'),
    path('<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('<int:pk>/complete/', views.assignment_complete, name='assignment_complete'),
    path('<int:pk>/update/', views.assignment_update, name='assignment_update'),
    path('<int:pk>/delete/', views.assignment_delete, name='assignment_delete'),
    
    # Course URLs
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/<int:pk>/update/', views.course_update, name='course_update'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),
    
    # Account URLs
    path('account/', account_view, name='account_view'),
    path('account/edit/', account_edit, name='account_edit'),
    
    # Learn/Podcast URLs
    path('learn/', learn_hub, name='learn_hub'),
    path('learn/podcast/create/', podcast_create, name='podcast_create'),
    path('learn/podcast/<int:pk>/generate/', podcast_generate, name='podcast_generate'),
    path('learn/podcast/<int:pk>/', podcast_detail, name='podcast_detail'),
    path('learn/podcast/<int:pk>/download/', podcast_download, name='podcast_download'),
    path('learn/podcast/<int:pk>/delete/', podcast_delete, name='podcast_delete'),
]

