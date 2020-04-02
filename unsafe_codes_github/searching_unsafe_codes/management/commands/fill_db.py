from builtins import print

from django.core.management.base import BaseCommand
from searching_unsafe_codes.models import Languages, Settings, Statuses, Unsafe_codes
import os
from users_and_permissions.models import AdvancedUser


# Начально заполнение БД
class Command(BaseCommand):

    def handle(self, *args, **options):
        # Проверяем наличие суперюзера. Если есть, то берем самого первого.
        superusers = AdvancedUser.objects.filter(is_superuser=True)
        if not superusers:
            print('Для начального заполнения базы данных, нужно ввести суперпользователя!')
            return

        superuser = superusers[0]

        # Настройки и сведения о программе
        # При первоначальном заполнении запись должна быть одна
        # В дальнейшем будет храниться несколько настроек с датой создания.
        Settings.objects.all().delete()
        Settings.objects.create(path_to_token=os.path.join(os.getcwd(), 'GitHub_Token'),
                                author='Фомин Дмитрий',
                                phone='8-123-123-12-12',
                                email='email@email.com',
                                create_user=superuser)

        # Список языков программирования
        # Название языка уникально
        languages_list = ['python', 'django']
        for item in languages_list:
            try:
                Languages.objects.create(name=item,
                                         create_user=superuser)
            except:
                print(f'Язык программирования "{item}" уже добавлен')

        # Статусы опасного кода
        # Статусы уникальны
        statuses_list = ['Содержит уязвимость', 'Потенциально опасен']
        for item in statuses_list:
            try:
                Statuses.objects.create(description=item,
                                        create_user=superuser)
            except:
                print(f'Статус "{item}" уже добавлен')

        # Заполнение списка уязвимостей
        # Строковый код уязвимости уникальный
        unsafe_codes = [{'language': 'python', 'string_code': 'eval', 'description': 'В коде есть функция eval.',  'add_description': 'В функцию eval, возможно, передано значение из внешнего источника.', 'status': 'Потенциально опасен'},
                        {'language': 'python', 'string_code': 'sqlite3', 'description': 'В коде есть sql инъекция.', 'add_description': '', 'status': 'Содержит уязвимость'},
                        {'language': 'python', 'string_code': 'pickle', 'description': 'В коде используется модуль pickle.', 'add_description': 'В функцию pickle.load(), возможно, передаются данные из стороннего источника.', 'status': 'Потенциально опасен'},
                        {'language': 'python', 'string_code': 'EMAIL_HOST_USER', 'description': 'Явно указан email.', 'add_description': '', 'status': 'Содержит уязвимость'},
                        {'language': 'python', 'string_code': 'EMAIL_HOST_PASSWORD', 'description': 'Явно указаны пароли от email.', 'add_description': '', 'status': 'Содержит уязвимость'}
                       ]
        for item in unsafe_codes:
            try:
                language = Languages.objects.get(name=item['language'])
                status = Statuses.objects.get(description=item['status'])
                if language and status:
                    Unsafe_codes.objects.create(string_code=item['string_code'],
                                                description=item['description'],
                                                add_description=item['add_description'],
                                                language_id=language.id,
                                                status_id=status.id,
                                                create_user=superuser)
            except:
                print(f'Строковый код {item["string_code"]} уже добавлен')
