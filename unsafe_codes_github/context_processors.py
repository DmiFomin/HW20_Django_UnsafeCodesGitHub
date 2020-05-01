from searching_unsafe_codes.models import History

def last_searching(request):
    result = ''
    if request.user.is_authenticated:
        last_history = History.objects.last();
        if last_history:
            result = last_history.date

    return {"last_searching": result}