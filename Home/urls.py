from django.urls import path
from Home import views

urlpatterns = [
    path('', views.index, name='home_index'),
    path('attendance/', views.attendance, name='home_attendance'),
    path('about/', views.about, name='home_about'),
    path('contact/', views.contact, name='home_contact'),
    path('video_feed/', views.video_feed, name='home_video_feed'),
    path('extract/', views.extract_features, name='home_extract_features'),
    path('ajax/refresh_table/', views.refresh_table, name='home_refresh_table'),
]