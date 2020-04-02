from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class AdvancedUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_view_history = models.BooleanField(default=False, verbose_name='Просмотр истории поиска')