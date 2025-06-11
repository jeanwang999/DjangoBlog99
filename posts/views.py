from django.shortcuts import render
from django.http import HttpResponse
from posts.models import Post


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
    