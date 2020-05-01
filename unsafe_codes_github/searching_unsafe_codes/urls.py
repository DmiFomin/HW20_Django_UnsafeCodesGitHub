from django.urls import path
from searching_unsafe_codes import views


app_name = 'searching_unsafe_codes'

urlpatterns = [
    # path('', views.main_view, name='index'),
    #path('searching/', views.searching, name='searching'),
    #path('searching_history/', views.searching_history, name='searching_history'),
    #path('contacts/', views.contacts, name='contacts'),
    # path('settings/', views.settings, name='settings'),

    path('', views.MainView.as_view(), name='index'),
    path('unsafe_codes_update/<int:pk>/', views.UnsafeCodesUpdataView.as_view(), name='unsafe_codes_update'),
    path('unsafe_codes_delete/<int:pk>/', views.UnsafeCodesDeleteView.as_view(), name='unsafe_codes_delete'),
    path('searching/', views.SearchingView.as_view(), name='searching'),
    #path('searching_details/', views.SearchingDetailsView.as_view(), name='searching_details'),
    path('searching_history/', views.SearchingHistoryView.as_view(), name='searching_history'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('contacts_create/', views.ContactsCreateView.as_view(), name='contacts_create'),


]