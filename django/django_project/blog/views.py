from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
        'author': 'MojalefaK',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'JaneDoe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'August 27, 2018'
    }
]

def home(request):
    title = 'Home'
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', title, content)

def about(request):
    title = 'About'
    return render(request, 'blog/about.html', title)
