from django.contrib.auth.forms import UserCreationForm
from .models import AdvancedUser


class RegistrationForm(UserCreationForm):
    class Meta:
        model = AdvancedUser
        fields = ('username', 'password1', 'password2', 'email')