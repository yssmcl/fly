from datetime import datetime

from django.utils import timezone, formats
from django.core.mail import send_mail

from fly.settings import EMAIL_HOST_USER
from comissao.models import Comissao, Comissao_Docente

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


def send_email_comissao(subject, html_message):
    emails = set()

    for comissao in Comissao.objects.filter(inicio__lte=timezone.now(), fim__gt=timezone.now()):
        for comissao_docente in comissao.comissao_docente_set.all():
            emails.add(comissao_docente.docente.email)

    send_mail(subject, '', EMAIL_HOST_USER, list(emails), html_message=html_message, fail_silently=False)
