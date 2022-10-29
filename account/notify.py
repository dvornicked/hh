import os
import django
from django.core.mail import EmailMultiAlternatives
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hh.settings')
django.setup()

from scraping.models import Vacancy
from account.models import Profile

qs = Profile.objects.filter(notify=True).select_related('user').values('user__email', 'city', 'language')
users_dct = {}
vacancies_dct = {}
for user in qs: users_dct.setdefault((user['city'], user['language']), []).append(user['user__email'])
params = {'city_id__in': [key[0] for key in users_dct.keys()],
            'language_id__in': [key[1] for key in users_dct.keys()]}
qs = Vacancy.objects.filter(**params).values().order_by('timestamp')
vacancies_dct = {(vacancy['city_id'], vacancy['language_id']): [] for vacancy in qs}
for vacancy in qs: vacancies_dct[(vacancy['city_id'], vacancy['language_id'])].append(vacancy)

for keys, emails in users_dct.items():
    vacancies = vacancies_dct.get(keys, [])
    if vacancies:
        subject = f'Found new vacancies'
        text_content = f'Found new vacancies'
        html_content = '<h2>Found new vacancies:</h2>'
        for vacancy in vacancies[:4]:
            html_content += f'<a href="{vacancy["url"]}">{vacancy["title"]}</a><br>'
            html_content += f'<p>{vacancy["description"]}</p><br><hr>'
        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, config('EMAIL_HOST_USER'), [email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
