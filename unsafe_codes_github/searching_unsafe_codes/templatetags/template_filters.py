# Отдельное приложение создавать не стал, так как этот вывод только в шаблоне поиска и истории.
from django import template
from searching_unsafe_codes.models import Unsafe_codes

register = template.Library()


def dict_to_list(dict):
    '''
    Преобразуем словарь в список для вывода в шаблоне поиска и истории.
    :param dict: словарь
    :return: список [name_module, description, status, url_module]
    '''
    result_list = ['','','','']
    for key, item in dict.items():
        if key == 'name_module':
            result_list[0] = item
        elif key == 'description':
            result_list[1] = item
        elif key == 'status':
            result_list[2] = item
        elif key == 'url_module':
            result_list[3] = item

    return result_list


def get_user_settings(user_settings, ):
    description_list = []
    string_code_list = user_settings
    result_description = Unsafe_codes.objects.filter(string_code__in=string_code_list)
    # for param in user_settings.split(';'):
    #     if param:
    #         try:
    #             result_description = Unsafe_codes.objects.get(string_code=param)
    #             if result_description:
    #                 param_list.append(result_description.description)
    #         except Unsafe_codes.DoesNotExist:
    #             result_description = None

    description_list = list(result_description)
    #print(description_list)
    description_list.reverse()
    return description_list


register.filter('dict_to_list', dict_to_list)
register.filter('get_user_settings', get_user_settings)