from django.core.paginator import Paginator
from django.shortcuts import render

from .forms import SearchForm
from .models import Vacancy


def home_view(request):
    form = SearchForm()
    return render(request, 'scraping/home.html', {'form': form})


def list_view(request):
    city = request.GET.get('city')
    language = request.GET.get('language')
    form = SearchForm(initial={'city': city, 'language': language})
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug__contains'] = city
        if language:
            _filter['language__slug__contains'] = language

        qs = Vacancy.objects.filter(**_filter).order_by('-timestamp')
    else:
        qs = Vacancy.objects.all().order_by('-timestamp')
    paginator = Paginator(qs, 12)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'form': form,
        'object_list': page,
        'city': city or '',
        'language': language or '',
    }
    return render(request, 'scraping/list.html', context)
