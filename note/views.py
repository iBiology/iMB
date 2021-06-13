from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django import forms
from .models import Word

import datetime
import requests
import string


class SearchForm(forms.Form):
    word = forms.CharField()


def directory(audio):
    if audio.startswith('bix'):
        return 'bix'
    elif audio.startswith('gg'):
        return 'gg'
    elif audio[:1].isdigit() or audio[:1] in string.punctuation:
        return 'number'
    else:
        return audio[:1]


def index(request):
    latest_word = Word.objects.order_by('-ymd')[0]
    today_words = Word.objects.filter(ymd__date=datetime.date.today())
    latest_word.senses = latest_word.sense.split('\n')
    latest_word.directory = directory(latest_word.audio)
    return render(request, 'note/base.html')
    # return render(request, 'note/index.html', {'data': latest_word,
    #                                            'today_words': today_words})


def search(request):
    word = request.GET.get('q')
    try:
        data = Word.objects.get(word=word)
        print('db record')
    except Word.DoesNotExist:
        print('no existing')
        _, data = search_mb(word)
    # _, data = search_mb(word)
    data.senses = data.sense.split('\n')
    data.directory = directory(data.audio)
    words = Word.objects.filter(ymd__gte=timezone.now().date() - datetime.timedelta(days=7))
    return render(request, 'note/query.html', {'query': data, 'words': words, 'days': 7})


def search_mb(word, key='b7070953-8bea-4687-b068-972d9f7a73c9'):
    url = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={key}'
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()[0]
        word = data['meta']['id']
        audio = data['hwi']['prs'][0]['sound']['audio']
        label = data['fl']
        senses = []
        for d in data['def']:
            ss = d['sseq']
            for s in ss:
                for xs in s:
                    for x in xs:
                        if isinstance(x, dict) and 'sn' in x:
                            sn, dt = x['sn'], x['dt'][0][1]
                            sn = sn if sn[0].isnumeric() else f'  {sn}'
                            dt = dt.replace('{bc}', ':')
                            senses.append(f'{sn}{dt}')
        print(word, audio, label, '\n'.join(senses))
        data = Word(word=word, audio=audio, label=label, sense='\n'.join(senses))
    else:
        data = None
    return r.status_code, data


def query(request, word, days):
    try:
        data = Word.objects.get(word=word)
        code = 200
        print('db record')
    except Word.DoesNotExist:
        print('no existing')
        code, data = search_mb(word)
    if code == 200:
        data.error = False
        data.senses = data.sense.split('\n')
        data.directory = directory(data.audio)
    else:
        data = Word('Error', '', '', '')
        data.error = True

    if days:
        day = timezone.now().date() - datetime.timedelta(days=days)
        words = Word.objects.filter(ymd__gte=day)
    else:
        words = Word.objects.all()
    return render(request, 'note/query.html', {'query': data, 'words': words, 'days': days})


def favorite(request):
    word = ''
    if request.is_ajax and request.method == 'POST':
        word = request.POST.get('word')
        word = Word.objects.get(word=word)
        word.update(favorite=False)
    return JsonResponse({'message': f'Unfavorite word {word} succeed.'}, status=200)
