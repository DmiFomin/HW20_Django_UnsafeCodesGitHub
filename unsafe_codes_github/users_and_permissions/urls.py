from django.urls import path
from users_and_permissions import views
from django.contrib.auth.views import LogoutView


app_name = 'users_and_permissions'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration_user/', views.RegistrationUserView.as_view(), name='registration_user'),
    path('recovery_password/', views.recovery_password, name='recovery_password'),
]
