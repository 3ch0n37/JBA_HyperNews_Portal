import json
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings


# Create your views here.
class IndexView(View):
    def get(self, request):
        return HttpResponse('Coming soon')


class MainView(View):
    def get(self, request):
        with open(settings.NEWS_JSON_PATH) as f:
            news_list = json.load(f)
        news = {}
        for story in news_list:
            date = story['created'].split(' ')[0]
            if date not in news:
                news[date] = []
            news[date].append(story)
        news = sorted(news.items(), reverse=True)
        return render(request, 'news/index.html', context={'news': news})


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
