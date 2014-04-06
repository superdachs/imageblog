from django.conf.urls import patterns, url
from core import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<site_id>\d+)/$', views.site, name='site'),
    url(r'^gallery/(?P<gallery_id>\d+)/$', views.gallery, name='gallery'),
    url(r'^gallery/(?P<gallery_id>\d+)/overview/$', views.gallery_overview, name='gallery_overview'),   
    url(r'^article/(?P<article_id>\d+)/$', views.gallery, name='article'),
    url(r'^(?P<site_id>\d+)/(?P<gallery_id>\d+)/(?P<image_id>\d+)/$', views.gallery, name='gallery'),
)
