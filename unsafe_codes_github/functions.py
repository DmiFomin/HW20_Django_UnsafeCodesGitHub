import os
import json
import pprint
import base64
import re
import requests
from searching_unsafe_codes.models import Settings, Unsafe_codes, History, History_repositories, History_unsafe_code
import utility as utility


def load_token(path):
    '''
    Загружаем токен GitHub
    :param path: - путь до файла
    :return: - токен
    '''
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                result = f.readline()
                return result
        except Exception as e:
            print(e)
            print('Файл с токеном GitHub не обнаружен!')


def external_source(content):
    '''
    Ищем в модуле вхождение "токсичных" строк
    :param content: контент модуля
    :return: булево
    '''
    return '.read()' in content or 'input' in content or 'open('


# Для каждой проверки своя функция.
def check_eval(decoded_content, element_unsafe_code):

    result_list = []
    if 'eval(' in decoded_content:
        if external_source(decoded_content):
            result_list.append({'description': element_unsafe_code.add_description, 'status': 'Содержит уязвимость.'})
        else:
            result_list.append({'description': element_unsafe_code.description, 'status': str(element_unsafe_code.status)})

    return result_list


def check_SQL(decoded_content):

    result_SELECT = re.search(r"f'*select.+from*", decoded_content.lower())
    result_SELECT_format = re.search(r"select.+from.+\.format", decoded_content.lower())
    result_INSERT = re.search(r"f'*insert into*", decoded_content.lower())
    result_INSERT_format = re.search(r"insert into.+\.format", decoded_content.lower())
    result_UPDATE = re.search(r"f'*update.+set*", decoded_content.lower())
    result_UPDATE_format = re.search(r"update.+set.+\.format", decoded_content.lower())
    result_DELETE = re.search(r"f'*delete.+from*", decoded_content.lower())
    result_DELETE_format = re.search(r"delete.+from.+\.format", decoded_content.lower())

    result_list = []
    if result_SELECT != None or result_SELECT_format != None:
        if external_source(decoded_content):
            result_list.append({'description': 'В коде есть SQL запрос SELECT с получением данных из внешнего источника и, возможно, выполняется напрямую в БД.', 'status': 'Содержит уязвимость.'})

    if result_INSERT != None or result_INSERT_format != None:
        if external_source(decoded_content):
            result_list.append({'description': 'В коде есть SQL запрос INSERT с получением данных из внешнего источника и, возможно, выполняется напрямую в БД.', 'status': 'Содержит уязвимость.'})

    if result_UPDATE != None or result_UPDATE_format != None:
        if external_source(decoded_content):
            result_list.append({'description': 'В коде есть SQL запрос UPDATE с получением данных из внешнего источника и, возможно, выполняется напрямую в БД.', 'status': 'Содержит уязвимость.'})

    if result_DELETE != None or result_DELETE_format != None:
        if external_source(decoded_content):
            result_list.append({'description': 'В коде есть SQL запрос SELECT с получением данных из внешнего источника и, возможно, выполняется напрямую в БД.', 'status': 'Содержит уязвимость.'})

    return result_list


def check_pickle(decoded_content, element_unsafe_code):
    result_list = []
    if 'pickle.load(' in decoded_content:
        if external_source(decoded_content):
            result_list.append({'description': element_unsafe_code.add_description, 'status': 'Содержит уязвимость.'})
        else:
            result_list.append({'description': element_unsafe_code.description, 'status': str(element_unsafe_code.status)})

    return result_list


def check_django_email(decoded_content, element_unsafe_code, name_module):
    result_list = []
    if name_module =='settings.py':
        if f'{element_unsafe_code.string_code} =' in decoded_content:
            result_list.append({'description': element_unsafe_code.description, 'status': str(element_unsafe_code.status)})

    return result_list


def write_results(item, danger_modules_describe, element_unsafe_code, session):
    '''
    Записываем результат поиска в словарь
    :return: словарь
    '''
    # Если есть модуль не проходит доп. проверку, то берем ошибку из доп. проверки
    html_url = f'https://api.github.com/repos/{item["repository"]["full_name"]}/contents/{item["path"]}'

    file_response = session.get(html_url)
    decoded_content = base64.b64decode(file_response.json()['content']).decode('utf-8')

    result_check_list = []
    if element_unsafe_code.string_code == 'eval':
        result_check_list = check_eval(decoded_content, element_unsafe_code)
    elif element_unsafe_code.string_code == 'sqlite3':
        result_check_list = check_SQL(decoded_content)
    elif element_unsafe_code.string_code == 'pickle':
        result_check_list = check_pickle(decoded_content, element_unsafe_code)
    elif element_unsafe_code.string_code == 'EMAIL_HOST_USER' or element_unsafe_code.string_code == 'EMAIL_HOST_PASSWORD':
        result_check_list = check_django_email(decoded_content, element_unsafe_code, item['name'])

    # Получаем данные для вывода
    #print(result_check_list)
    for result_check in result_check_list:
        #print(result_check)
        repository_url = item['repository']['html_url']
        language = element_unsafe_code.language
        name_module = item['name']
        description = result_check['description']
        status = result_check['status']
        url_module = item['html_url']
        #pprint.pprint(item)

        # Для вывода в шаблоне Django меняем словарь на список. Со словарем в шаблоне сложно работать.
        # Оставляем словарь для использования шаблонного фильтра.
        unsafe_modules = {'name_module': name_module, 'description': description, 'status': status, 'url_module': url_module}
        #unsafe_modules = [name_module, description, status, url_module]

        if repository_url in danger_modules_describe:
            if not (language in danger_modules_describe[repository_url]['languages']):
                danger_modules_describe[repository_url]['languages'].append(language)
            danger_modules_describe[repository_url]['unsafe_modules'].append(unsafe_modules)
        else:
            danger_modules_describe[repository_url] = {'languages': [language], 'unsafe_modules' : [unsafe_modules]}

    return danger_modules_describe


def write_json(danger_modules_describe):
    '''
    Записываем результат поиска в файл JSON
    :param danger_modules_describe: словарь
    '''
    with open('danger_modules_GitHub.json', 'w', encoding='utf-8') as f:
        json.dump(danger_modules_describe, f, ensure_ascii=False)
        #pprint.pprint(danger_modules_describe)


def write_to_base(danger_modules_describe, user_settings, repository_name, current_user):
    '''
    Записываем результат в БД
    :param danger_modules_describe: словарь с опасным кодом
    :param user_settings: настройки пользователя
    '''
    history_record = History()
    history_record.params = user_settings
    history_record.repository_name = repository_name
    history_record.user = current_user
    history_record.save()

    string_code_list = user_settings
    user_settings_for_record = Unsafe_codes.objects.filter(string_code__in=string_code_list)
    history_record.user_settings.add(*list(user_settings_for_record))

    for item in danger_modules_describe.items():
        history_repositories = History_repositories()
        history_repositories.history=history_record
        history_repositories.repository=item[0]
        history_repositories.language=item[1]['languages'][0]
        history_repositories.save()

        for item_unsafe_modules in item[1]['unsafe_modules']:
            History_unsafe_code(repository=history_repositories, unsafe_code=utility.dict_to_str(item_unsafe_modules)).save()

    return history_record.id


def get_history_list(id=None):
    '''
    Получаем из БД Историю поиска
    :param id: идентификатор записи
    :return: список
    '''
    #result = orm.get_history_list(id)
    #return result
    pass


def get_danger_modules_describe(id):

    # result_repository = History_repositories.objects.filter(history=id)
    # for item_repository in result_repository:
    #     result_unsafe_code = History_unsafe_code.objects.filter(repository=item_repository.id)
    #     list_unsafe_code = []
    #     for item_unsafe_code in result_unsafe_code:
    #         list_unsafe_code.append(utility.dict_from_str(item_unsafe_code.unsafe_code))
    #
    #     danger_modules_describe[item_repository.repository] = {'languages': [item_repository.language],
    #                                                            'unsafe_modules': list_unsafe_code}

    result_unsafe_code = History_unsafe_code.objects.filter(repository__history__id=id).order_by('repository').select_related('repository__language')

    #TODO Возвращаю словарь. В дальнейшем надо обойтись одним запросом, без словаря.
    danger_modules_describe = {}
    list_unsafe_code = []
    last_url = ''
    for item in result_unsafe_code:
        if last_url != item.repository.repository and last_url != '':
            danger_modules_describe[last_url] = {'languages': [item.repository.language],
                                                'unsafe_modules': list_unsafe_code}
            list_unsafe_code = []

        last_url = item.repository.repository
        list_unsafe_code.append(utility.dict_from_str(item.unsafe_code))

    return danger_modules_describe


def seaching_unsafe_code(user_settings, repository_name, current_user):
    '''
    Поиск опасного кода
    :param user_settings: настройки пользователя
    :param PROGRAM_SETTINGS: настройки программы
    :return: словарь
    '''
    #Загружаем токен из файла
    last_setting = Settings.objects.last()
    token = load_token(last_setting.path_to_token)

    session = requests.Session()
    session.auth = ('DmiFomin', token)

    unsafe_code = Unsafe_codes.objects.all()
    danger_modules_describe = {}

    for element_unsafe_code in unsafe_code:
        if not (element_unsafe_code.string_code in user_settings):
            continue

        language = element_unsafe_code.language
        string_languages = f'language:{language}'
        string_searching = element_unsafe_code.string_code

        #print('--------------------------- Ищем', string_searching, 'в модулях на', string_languages, '---------------------------')
        #string_connect = f'https://api.github.com/search/code?q={string_searching}in:file+{string_languages}+user:DanteOnline'
        #string_connect = f'https://api.github.com/search/code?q={string_searching}in:file+{string_languages}page=20&per_page=100{f"+user:{repository_name}" if repository_name else ""}'
        string_connect = f'https://api.github.com/search/code?q={string_searching}in:file+{string_languages}{f"+user:{repository_name}" if repository_name else ""}'
        #print(string_connect)
        try:
            result = session.get(string_connect)
            #print(result.status_code)
            items = result.json()['items']

            for item in items:
                if not item['path'].startswith('venv'):
                    danger_modules_describe = write_results(item, danger_modules_describe, element_unsafe_code, session)

        except Exception as e:
            print(e)

    #print(danger_modules_describe)
    #write_json(danger_modules_describe)
    history_id = write_to_base(danger_modules_describe, user_settings, repository_name, current_user)
    return history_id, danger_modules_describe
