from django.contrib import admin
from .models import History, History_repositories, History_unsafe_code, Languages, Settings, Statuses, Unsafe_codes

# Register your models here.
admin.site.register(History)
admin.site.register(History_repositories)
admin.site.register(History_unsafe_code)
admin.site.register(Languages)
admin.site.register(Settings)
admin.site.register(Statuses)
admin.site.register(Unsafe_codes)
