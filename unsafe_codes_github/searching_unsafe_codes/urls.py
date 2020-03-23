from django.urls import path
from searching_unsafe_codes import views


app_name = 'searching_unsafe_codes'

urlpatterns = [
    path('', views.main_view, name='index'),
    path('searching/', views.searching, name='searching'),
    path('searching_history/', views.searching_history, name='searching_history'),
    path('contacts/', views.contacts, name='contacts'),
    path('settings/', views.settings, name='settings'),
]