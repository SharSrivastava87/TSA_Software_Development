from django.urls import path

from . import views

app_name = 'CyRanch_Connect'

# URL patterns for the CyRanch Connect app
urlpatterns = [
    path('event-checkin/<slug:event_id>', views.event_checkin, name='event_checkin'),
    path('event-qr/<slug:event_id>', views.event_qr, name='event-qr'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name = 'logout'),
    path('prizes/', views.prizes, name='prizes'),
    path('events/', views.events, name='events'),
    path('help/', views.help, name='help'),
    path('report/', views.generate_report, name='report'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('Terms&Conditions/', views.terms),
]
