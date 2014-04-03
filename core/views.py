from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
import os.path
from PIL import Image
from PIL.ExifTags import TAGS
import re
import exifread

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
    f = open(image.base_file.file.name, 'rb')
    exifd = exifread.process_file(f)
    f.close()
    for tag in exifd:
        print(str(tag) + ":" + str(exifd[tag]))
    
    
    ld = exifd['MakerNote LensData']
    print(ld) 
    
    #############################################################



    exifdata = {}
    i = Image.open(image.base_file.file.name)
    inf = i._getexif()
    
    for tag, value in inf.items():
        decoded = TAGS.get(tag, tag)
        try:
            urls = re.findall('http[s]?://[0-9a-z./&%$?-]*', value)
            for url in urls:
                print(url)
                value = value.replace(url, '<a href="' + url + '">' + url + '</a>')
        except TypeError:
            pass
        if not value == "":
            exifdata[decoded] = value

    try:
        exifdata['FNumberH'] = exifdata['FNumber'][0] / exifdata['FNumber'][1]
    except Exception:
        pass
    try:
        exifdata['ExposureTimeH'] = exifdata['ExposureTime'][0] / exifdata['ExposureTime'][1]
    except Exception:
        pass
    try:    
        exifdata['FocalLengthH'] = exifdata['FocalLength'][0] / exifdata['FocalLength'][1]
    except Exception:
        pass
    
    context = {'gallery': gallery,
        'image': image,
        'exif': exifdata,
        }
    return render(request, 'core/gallery.phtml', context)



