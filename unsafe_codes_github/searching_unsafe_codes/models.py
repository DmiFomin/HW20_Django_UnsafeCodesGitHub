from django.db import models
from users_and_permissions.models import AdvancedUser
import os
from django.utils import timezone


# Create your models here.
class Settings(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    path_to_token = models.CharField(max_length=15, default=os.path.join(os.getcwd(), 'GitHub_Token'))
    author = models.CharField(max_length=80, verbose_name='Автор')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(max_length=30, verbose_name='E-mail')
    create_user = models.ForeignKey(AdvancedUser, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'

    def __str__(self):
        return f'Дата создания: {self.date}, ' \
               f'Кто создал: {self.create_user}, ' \
               f'Автор: {self.author}, ' \
               f'Телефон: {self.phone}, ' \
               f'E-mail: {self.email}'

    # Если путь до токена не заполнен, то поиск работать не будет.
    def is_path_to_token(self):
        return self.path_to_token != ''


class Statuses(models.Model):
    description = models.CharField(max_length=50, unique=True)
    create_user = models.ForeignKey(AdvancedUser, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.description


class Languages(models.Model):
    name = models.CharField(max_length=15, unique=True)
    create_user = models.ForeignKey(AdvancedUser, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'

    def __str__(self):
        return self.name


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

    # Проверяем заполнение обязательных полей
    def is_language(self):
        return self.language is not None

    def is_string_code(self):
        return self.string_code != ''

    def is_description(self):
        return self.description != ''

    def is_status(self):
        return self.status is not None


class History(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    params = models.TextField()
    user_settings = models.ManyToManyField(Unsafe_codes)
    repository_name = models.CharField(max_length=150)
    user = models.ForeignKey(AdvancedUser, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'История поиска'
        verbose_name_plural = 'История поиска'

    # Переопределеяем метод save. Записываем текущего юзера.
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     # Хотел получить текущего пользователя.


class History_repositories(models.Model):
    history = models.ForeignKey(History, on_delete=models.PROTECT)
    repository = models.TextField(blank=True)
    language = models.ForeignKey(Languages, on_delete=models.PROTECT)


class History_unsafe_code(models.Model):
    repository = models.ForeignKey(History_repositories, on_delete=models.PROTECT)
    unsafe_code = models.TextField()
