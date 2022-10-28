import os

import django
import asyncio
import requests
from bs4 import BeautifulSoup as BSoup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hh.settings')
django.setup()

from scraping.models import Vacancy, City, Language
from account.models import Profile

headers = {'User-Agent': '"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/74.0.3729.169 Safari/537.36"'}

vacancies = []


def hh(city, language):
    url = f'https://hh.ru/search/vacancy?area={city.hh_id}&text={language.name}'
    response = requests.get(url=url, headers=headers)
    results = []
    if response.status_code == 200:
        soup = BSoup(response.content, 'html.parser')
        container = soup.find('div', attrs={'data-qa': 'vacancy-serp__results'})
        vacancy_nodes = container.find_all('div', attrs={'class': 'serp-item'})
        for node in vacancy_nodes:
            title_node = node.find('a')
            title = title_node.text
            url = title_node['href']
            company = node.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
            description = (node.find('div',
                                     attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}) or node.find(
                'div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'})).text
            results.append(
                {'title': title, 'url': url, 'company': company, 'description': description, 'language': language,
                 'city': city})
    return results


def get_notify_list():
    profiles = Profile.objects.filter(notify=True)
    return set([(profile.city, profile.language) for profile in profiles if profile.city and profile.language])


async def main(value):
    results = await loop.run_in_executor(None, hh, *value)
    vacancies.extend(results)


notify_list = get_notify_list()
if notify_list:
    loop = asyncio.get_event_loop()
    tasks = asyncio.wait([loop.create_task(main(value)) for value in get_notify_list()])
    loop.run_until_complete(tasks)
    loop.close()
    for vacancy in vacancies:
        try:
            Vacancy.objects.create(**vacancy)
        except Exception as e:
            print(e)
