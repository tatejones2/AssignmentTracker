"""
URL configuration for assignments app.
"""
from django.urls import path
from . import views
from .views_auth import account_view, account_edit
from .views_learn import (
    learn_hub, podcast_create, podcast_generate, 
    podcast_detail, podcast_download, podcast_delete,
    study_notes_hub, study_notes_create, study_notes_detail, study_notes_delete
)
from .views_chat import (
    chatbot_hub, chatbot_ask, chatbot_delete_message, chatbot_clear_all
)
from .views_events import (
    events_hub, event_list, event_create, event_detail, event_update, event_delete,
    reminder_list, reminder_create, reminder_detail, reminder_update, reminder_delete,
    reminder_mark_complete, api_upcoming_events, api_upcoming_reminders
)

urlpatterns = [
    # Health check
    path('health/', views.health_check, name='health_check'),
    
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
    
    # Study Notes URLs
    path('learn/notes/', study_notes_hub, name='study_notes_hub'),
    path('learn/notes/create/', study_notes_create, name='study_notes_create'),
    path('learn/notes/<int:pk>/', study_notes_detail, name='study_notes_detail'),
    path('learn/notes/<int:pk>/delete/', study_notes_delete, name='study_notes_delete'),
    
    # Chatbot URLs
    path('chatbot/', chatbot_hub, name='chatbot_hub'),
    path('chatbot/ask/', chatbot_ask, name='chatbot_ask'),
    path('chatbot/<int:pk>/delete/', chatbot_delete_message, name='chatbot_delete'),
    path('chatbot/clear/', chatbot_clear_all, name='chatbot_clear'),
    
    # Events & Reminders URLs
    path('events/', events_hub, name='events_hub'),
    path('events/list/', event_list, name='event_list'),
    path('events/create/', event_create, name='event_create'),
    path('events/<int:pk>/', event_detail, name='event_detail'),
    path('events/<int:pk>/update/', event_update, name='event_update'),
    path('events/<int:pk>/delete/', event_delete, name='event_delete'),
    
    # Reminders URLs
    path('reminders/', reminder_list, name='reminder_list'),
    path('reminders/create/', reminder_create, name='reminder_create'),
    path('reminders/<int:pk>/', reminder_detail, name='reminder_detail'),
    path('reminders/<int:pk>/update/', reminder_update, name='reminder_update'),
    path('reminders/<int:pk>/delete/', reminder_delete, name='reminder_delete'),
    path('reminders/<int:pk>/complete/', reminder_mark_complete, name='reminder_mark_complete'),
    
    # API Endpoints
    path('api/upcoming-events/', api_upcoming_events, name='api_upcoming_events'),
    path('api/upcoming-reminders/', api_upcoming_reminders, name='api_upcoming_reminders'),
]

