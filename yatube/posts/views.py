from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    template = 'posts/index.html'
    title = "Это главная страница проекта Yatube"
    text = "Писеньку пососи"
    context = {
        'title': title,
        'text': text,
    }
    return render(request, template, context)

def group_posts(request, slug):
    template = 'posts/group_list.html'
    text = "Здесь будет информация о группах проекта Yatube"
    context = {
        'text': text
    }
    return render(request, template, context)