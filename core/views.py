from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
import os.path
from PIL import Image
from PIL.ExifTags import TAGS

from core.models import Site, Article, Gallery, GalImage

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
    # TODO: Objektivdaten rauskriegen (Namen, Typ, Hersteller und son Käse
    gallery = get_object_or_404(Gallery, pk=gallery_id)
    image = get_object_or_404(GalImage, pk=image_id)

    exifdata = {}
    i = Image.open(image.base_file.file.name)
    inf = i._getexif()
    for tag, value in inf.items():
        decoded = TAGS.get(tag, tag)

#links ersetzen
        print(str(decoded) + " " + str(value))
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

