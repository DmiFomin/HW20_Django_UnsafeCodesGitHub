from django.db import models


# Create your models here.
class Settings(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    path_to_token = models.CharField(max_length=15)
    author = models.CharField(max_length=80)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)


class Statuses(models.Model):
    description = models.CharField(max_length=50, unique=True)


class Languages(models.Model):
    name = models.CharField(max_length=15, unique=True)


class Unsafe_codes(models.Model):
    language = models.ForeignKey(Languages, on_delete=models.PROTECT)
    string_code = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=150)
    add_description = models.CharField(max_length=150)
    status = models.ForeignKey(Statuses, on_delete=models.PROTECT)


class History(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    params = models.TextField()


class History_repositories(models.Model):
    history = models.ForeignKey(History, on_delete=models.PROTECT)
    repository = models.URLField
    language = models.ForeignKey(Languages, on_delete=models.PROTECT)


class History_unsafe_code(models.Model):
    repository = models.ForeignKey(History_repositories, on_delete=models.PROTECT)
    unsafe_code = models.TextField()

