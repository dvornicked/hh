from django.shortcuts import render

from .forms import SearchForm
from .models import Vacancy


def home_view(request):
    form = SearchForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    qs = []
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug__contains'] = city
        if language:
            _filter['language__slug__contains'] = language

        qs = Vacancy.objects.filter(**_filter)

    return render(request, 'scraping/home.html', {'object_list': qs, 'form': form})
