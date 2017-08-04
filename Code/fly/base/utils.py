from datetime import datetime

from django.utils import formats

def parse_locale_date(formatted_date):
    parsed_date = None
    for date_format in formats.get_format('DATE_INPUT_FORMATS'):
        try:
            parsed_date = datetime.strptime(formatted_date, date_format)
        except ValueError:
            continue
        else:
            break
    if not parsed_date:
        raise ValueError
    return parsed_date.date()