import json
import random
import datetime
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.conf import settings


# Create your views here.
class IndexView(View):
    def get(self, request):
        return redirect('/news/')


class MainView(View):
    def get(self, request):
        with open(settings.NEWS_JSON_PATH) as f:
            news_list = json.load(f)
        news = {}
        search = False
        if 'q' in request.GET:
            search = request.GET['q']
        for story in news_list:
            if search and story['title'].find(search) == -1:
                continue
            date = story['created'].split(' ')[0]
            if date not in news:
                news[date] = []
            news[date].append(story)
        news = sorted(news.items(), reverse=True)
        return render(request, 'news/main.html', context={'news': news})


class StoryView(View):
    def get(self, request, story_id, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH) as f:
            news_list = json.load(f)
        selected = {}
        for story in news_list:
            if story['link'] == int(story_id):
                selected = story
                break
        return render(request, 'news/story.html', context={'story': selected})


class CreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/create.html')

    def post(self, request, *args, **kwargs):
        if 'title' not in request.POST or 'text' not in request.POST:
            return HttpResponseBadRequest('Not all arguments')
        with open(settings.NEWS_JSON_PATH) as f:
            news_list = json.load(f)
        ids = []
        for story in news_list:
            ids.append(story['link'])
        created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        while True:
            story_id = random.randint(0, 999999999)
            if story_id not in ids:
                break
        story = {
            'link': story_id,
            'created': created,
            'title': request.POST.get('title'),
            'text': request.POST.get('text')
        }
        news_list.append(story)
        with open(settings.NEWS_JSON_PATH, 'w') as f:
            json.dump(news_list, f)
        return redirect('/news/')
