from django.shortcuts import render
from django.http import HttpResponse
from posts.models import Post
from datetime import datetime


# Create your views here.

# def定義想要新增的頁面的名稱 再去urls.py 新增path
def index(request):
    article_records = Post.objects.all()
    article_list = list()
    for count, article in enumerate(article_records):
        article_list.append("#{}: {}<br><hr>".format(str(count), str(article)))
        article_list.append("<small>{}</small><br> slug:{}<br><hr> ".format(article.content,article.slug))
    return HttpResponse(article_list)

# def定義想要新增的頁面的名稱 再去urls.py 新增path


def about(request):
    return HttpResponse("hello world")


def index_use_template(requests):
    article_records = Post.objects.all()
    now = datetime.now()
    # return render(requests, "index.html", locals())
    return render(requests, 'pages/home.html', locals())


def showPost(requests, slug):
    article = Post.objects.get(slug=slug)
    return render(requests, 'pages/post.html', locals())

# 使用JsonResponse 
from django.http import JsonResponse
def showArticleList(requests):
    article = Post.objects.all().values()
    article = list(article)
    return JsonResponse(article, safe=False)

def login(requests):
    return render(requests, 'pages/login.html')
