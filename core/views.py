from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
import os.path
import os
import subprocess
from PIL import Image
import re

from core.models import Site, Article, Gallery, GalImage

def url2link(value):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', value)
    for url in urls:
        value.replace(url, '<a href="' + url + '">' + url + '</a>')
    return value

def index(request):
    latest_site_list = Site.objects.order_by('-pub_date')
    context = {'latest_site_list': latest_site_list}
    return render(request, 'core/sites.phtml', context)

def site(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    articles = Article.objects.filter(site = site_id).order_by('-pub_date')
    galleries = Gallery.objects.filter(site = site_id).order_by('-pub_date')
    context = {'site': site,
        'articles': articles,
        'galleries': galleries,
        }
    return render(request, 'core/site.phtml', context)

def gallery(request, site_id, gallery_id, image_id):
    gallery = get_object_or_404(Gallery, pk=gallery_id)
    image = get_object_or_404(GalImage, pk=image_id)

    #############################################################
    # neue metadaten behandlung                                 #
    #############################################################
    cmdline = "exiv2 -pab " + image.base_file.file.name
    p = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    exifdata = {}
    for line in iter(p.stdout.readline, b''):
        print(str(line))
        try:
            print("1")
            l = re.sub('b\'', '', str(line))
            l = re.sub('\'', '', l)
            l = l.replace("\\n", " ")
            l = re.sub('\s+', ' ', l).strip()
            print("2")
            print(l)
            key = re.sub('\.', '_', l.split( )[0])
            value = l.split(' ', 3 )[3]
            if not value == '(Binary value suppressed)':
                exifdata[key] = value
        except Exception:
            pass
    p.wait()

    for d in exifdata:
        print(d + ' - ' + exifdata[d])

    #############################################################
   
    context = {'gallery': gallery,
        'image': image,
        'exif': exifdata,
        }
    return render(request, 'core/gallery.phtml', context)



