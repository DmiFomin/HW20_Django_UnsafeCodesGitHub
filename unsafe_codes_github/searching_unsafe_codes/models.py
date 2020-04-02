from django.db import models
from users_and_permissions.models import AdvancedUser


# Create your models here.
class Settings(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    path_to_token = models.CharField(max_length=15)
    author = models.CharField(max_length=80, verbose_name='Автор')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(max_length=30, verbose_name='E-mail')
    create_user = models.ForeignKey(AdvancedUser, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'


class Statuses(models.Model):
    description = models.CharField(max_length=50, unique=True)
    create_user = models.ForeignKey(AdvancedUser, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Languages(models.Model):
    name = models.CharField(max_length=15, unique=True)
    create_user = models.ForeignKey(AdvancedUser, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'


class Unsafe_codes(models.Model):
    language = models.ForeignKey(Languages, on_delete=models.PROTECT)
    string_code = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=150, verbose_name='Описание опасного кода')
    add_description = models.CharField(max_length=150)
    status = models.ForeignKey(Statuses, on_delete=models.PROTECT)
    create_user = models.ForeignKey(AdvancedUser, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Опасный код'
        verbose_name_plural = 'Список опасных кодов'


class History(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    params = models.TextField()
    user = models.ForeignKey(AdvancedUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'История поиска'
        verbose_name_plural = 'История поиска'


class History_repositories(models.Model):
    history = models.ForeignKey(History, on_delete=models.PROTECT)
    repository = models.URLField
    language = models.ForeignKey(Languages, on_delete=models.PROTECT)


class History_unsafe_code(models.Model):
    repository = models.ForeignKey(History_repositories, on_delete=models.PROTECT)
    unsafe_code = models.TextField()
