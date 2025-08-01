"""
URL configuration for DjangoBlog99 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from posts.views import index
from posts.views import about
from posts.views import index_use_template
from posts.views import showPost
from posts.views import login
from line_bot.views import callback
from django.conf import settings
from django.conf.urls.static import static
from posts.views import showArticleList


urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", index),
    path("", index_use_template),
    path("about/", about),
    path("post/<str:slug>", showPost),
    path('login', login),
    path('line/', callback),
    path('api/posts/', showArticleList),



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
