"""projekty URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from projekty.views import main, register
from database.views import database, projekty, sortby, search, my_projects, new_project, zmen_projekt

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'main'}, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^main/$', my_projects, name = 'main'),
    url(r'^register/$', register),
    url(r'^database/$', database),
    url(r'^database/projekty/(\d+)/$', projekty),
    url(r'^database/projekty/(\d+)/zmen/$', zmen_projekt),
    url(r'^database/zorad/([a-z]+)/$', sortby),
    url(r'^database/search/$', search),
    url(r'^database/novy/$', new_project),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
