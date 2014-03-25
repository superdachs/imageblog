from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
import os.path

from core.models import Site, Article, Gallery

def index(request):
    latest_site_list = Site.objects.order_by('-pub_date')
    context = {'latest_site_list': latest_site_list}
    return render(request, 'core/sites.phtml', context)

def site(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    articles = Article.objects.filter(site = site_id).order_by('-pub_date')
    galleries = Gallery.objects.filter(site = site_id).order_by('-pub_date')
    basepath = os.path.dirname( __file__) + '/..'
    context = {'site': site,
        'articles': articles,
        'galleries': galleries,
        'basepath': basepath}
    return render(request, 'core/site.phtml', context)

