# Поиск уязвимостей в модулях GitHub

На данный момент ищутся следующие уязвимости:
* В коде есть функция eval.
* В коде есть sql инъекция.
* В коде используется модуль pickle.
* Явно указан email.
* Явно указаны пароли от email.

# Проблемы:
1. Не эффективное использование регулярных выражений для поиска опасного кода.
2. При поиске по всем репозиториям время поиска занимает длительное время.
