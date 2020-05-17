from django.urls import path, re_path
from users_and_permissions import views
from django.contrib.auth.views import LogoutView


app_name = 'users_and_permissions'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration_user/', views.RegistrationUserView.as_view(), name='registration_user'),
    path('profile_user/<int:pk>/', views.ProfileUserView.as_view(), name='profile_user'),
    path('create_token/', views.create_token),
    #path('recovery_password/', views.recovery_password, name='recovery_password'),
    path('password_reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', views.UserPasswordDoneView.as_view(), name='password_reset_done'),
    # TODO Проблема. Не получается верно прописать регулярное выражение, чтобы правильно формировалась ссылка.
    # Думаю, что для восстановления пароля нужно вводить логин юзера и его подставлять в регулярку.
    re_path('password_reset_confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)$', views.UserPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', views.UserPasswordCompleteView.as_view(), name='password_reset_complete'),
]
