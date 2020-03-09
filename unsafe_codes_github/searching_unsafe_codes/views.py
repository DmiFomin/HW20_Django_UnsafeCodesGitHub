from django.shortcuts import render
from .models import Unsafe_codes, Settings

# Create your views here.
def main_view(request):
    unsafe_codes = Unsafe_codes.objects.all()
    return render(request, 'searching_unsafe_codes/index.html', context={'unsafe_codes': unsafe_codes})


def searching(request):
    unsafe_codes = Unsafe_codes.objects.all()
    return render(request, 'searching_unsafe_codes/searching.html', context={'unsafe_codes': unsafe_codes, 'user_settings': {}})


def searching_history(request):
    return render(request, 'searching_unsafe_codes/searching_history.html', context={})


def contacts(request):
    settings = Settings.objects.all()[0]
    return render(request, 'searching_unsafe_codes/contacts.html', context={'settings': settings})


def settings(request):
    settings = Settings.objects.all()[0]
    return render(request, 'searching_unsafe_codes/settings.html', context={'settings': settings})