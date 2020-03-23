from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from .models import Unsafe_codes, Settings
from .forms import SettingsForm

# Create your views here.
def main_view(request):
    unsafe_codes = Unsafe_codes.objects.all()
    return render(request, 'searching_unsafe_codes/index.html', context={'unsafe_codes': unsafe_codes})


def searching(request):
    unsafe_codes = Unsafe_codes.objects.all()
    if request.method == 'POST':
        pass
    else:
        return render(request, 'searching_unsafe_codes/searching.html', context={'unsafe_codes': unsafe_codes, 'user_settings': {}})


def searching_history(request):
    return render(request, 'searching_unsafe_codes/searching_history.html', context={})


def contacts(request):
    #settings = Settings.objects.all()[0]
    settings = Settings.objects.last()
    if request.method == 'POST':
        pass
    else:
        return render(request, 'searching_unsafe_codes/contacts.html', context={'settings': settings})


def settings(request):
    #settings = Settings.objects.all()[0]
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('searching_unsafe_codes:contacts'))
        else:
            return render(request, 'searching_unsafe_codes/settings.html', context={'form': form})
    else:
        form = SettingsForm()
        return render(request, 'searching_unsafe_codes/settings.html', context={'form': form})#, 'settings': settings})