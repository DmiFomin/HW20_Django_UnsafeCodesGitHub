from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Unsafe_codes, Settings, History
from .forms import SettingsForm
import functions as fn


user_settings = list(Unsafe_codes.objects.all().values_list('string_code', flat=True)) #'eval;sqlite3;pickle;EMAIL_HOST_USER;EMAIL_HOST_PASSWORD;'
repository_name = ''
#danger_modules_describe = {}


class UserSettingsContexMixin(ContextMixin):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['user_settings'] = user_settings
        context['repository_name'] = repository_name

        return context

# Create your views here.
# def main_view(request):
#     unsafe_codes = Unsafe_codes.objects.all()
#     return render(request, 'searching_unsafe_codes/index.html', context={'unsafe_codes': unsafe_codes})


class MainView(ListView):
    model = Unsafe_codes
    template_name = 'searching_unsafe_codes/index.html'
    context_object_name = 'unsafe_codes'

    def get_queryset(self):
        return Unsafe_codes.objects.select_related('language', 'status').all()


class UnsafeCodesUpdataView(UpdateView):
    fields = ('description',)
    model = Unsafe_codes
    success_url = reverse_lazy('searching_unsafe_codes:index')
    template_name = 'searching_unsafe_codes/unsafe_codes_update.html'


class UnsafeCodesDeleteView(DeleteView):
    model = Unsafe_codes
    success_url = reverse_lazy('searching_unsafe_codes:index')
    template_name = 'searching_unsafe_codes/unsafe_codes_delete.html'


# def searching(request):
#     unsafe_codes = Unsafe_codes.objects.all()
#     if request.method == 'POST':
#         pass
#     else:
#         return render(request, 'searching_unsafe_codes/searching.html', context={'unsafe_codes': unsafe_codes, 'user_settings': {}})


class SearchingView(LoginRequiredMixin, ListView, UserSettingsContexMixin):
    model = Unsafe_codes
    template_name = 'searching_unsafe_codes/searching.html'
    context_object_name = 'unsafe_codes'

    def post(self, request, *args, **kwargs):
        global user_settings
        global repository_name
        #global danger_modules_describe

        user_settings = []
        params = request.POST
        for param in params:
            if param != 'repository_name':
                user_settings.append(param)
            else:
                repository_name = params['repository_name']

        history_id, danger_modules_describe = fn.seaching_unsafe_code(user_settings, repository_name, self.request.user)
        history_list = History.objects.filter(user=self.request.user, id=history_id)

        return render(request, 'searching_unsafe_codes/searching_details.html', context={'history_list': history_list, 'danger_modules_describe': danger_modules_describe})

# def searching_history(request):
#     return render(request, 'searching_unsafe_codes/searching_history.html', context={})


class SearchingHistoryView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    # TODO Под админом добавить вывод всей истории с указанием пользователя
    model = History
    template_name = 'searching_unsafe_codes/searching_history.html'
    context_object_name = 'searching_history'
    paginate_by = 4

    def get_queryset(self):
        return History.objects.filter(user=self.request.user).order_by('-date').prefetch_related('user_settings')

    def post(self, request, *args, **kwargs):
        params = request.POST
        #try:
        history_id = list(params.keys())[1]
        history_list = History.objects.filter(user=self.request.user, id=history_id)
        danger_modules_describe = fn.get_danger_modules_describe(history_id)
        # except:
        #     print('Error of getting history!')
        #     history_list = []
        #     danger_modules_describe = {}

        return render(request, 'searching_unsafe_codes/searching_details.html', context={'history_list': history_list, 'danger_modules_describe': danger_modules_describe})

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_view_history


# def contacts(request):
#     settings = Settings.objects.last()
#     if request.method == 'POST':
#         pass
#     else:
#         return render(request, 'searching_unsafe_codes/contacts.html', context={'settings': settings})


class ContactsView(ListView):
    model = Settings
    template_name = 'searching_unsafe_codes/contacts.html'
    context_object_name = 'settings'

    def get_queryset(self):
        return Settings.objects.last()


class ContactsCreateView(UserPassesTestMixin, CreateView):
    #fields = '__all__'
    #exclude = ('path_to_token',)
    fields = ('author', 'phone', 'email')
    model = Settings
    success_url = reverse_lazy('searching_unsafe_codes:contacts')
    template_name = 'searching_unsafe_codes/contacts_create.html'

    def form_valid(self, form):
        form.instance.create_user = self.request.user
        #print(self.request.user)
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser

# def settings(request):
#     if request.method == 'POST':
#         form = SettingsForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('searching_unsafe_codes:contacts'))
#         else:
#             return render(request, 'searching_unsafe_codes/settings.html', context={'form': form})
#     else:
#         form = SettingsForm()
#         return render(request, 'searching_unsafe_codes/settings.html', context={'form': form})#, 'settings': settings})


