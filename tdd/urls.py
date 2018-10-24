from django.conf.urls import include, url
from lists import views as list_views


urlpatterns = [
    url(r'^$', list_views.home_page, name='home'),
    url(r'^lists/', include('lists.urls')),
]
