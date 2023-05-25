import datetime


def year(request):
    """Добавляет переменную с текущим годом."""
    dt = datetime.datetime.now()
    seq = int(dt.strftime("%Y"))

    return {
        'year': seq,
    }
