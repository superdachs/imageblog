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
    allowedTags = { "DateTimeOriginal",
                    "Artist",
                    "Copyright",
                    "Flash",
                    "Software",
                    "ExposureTime",
                    "FocalLength",
                    "Make",
                    "Model",
                    "FocalLengthIn35mmFilm",
                    "ISOSpeedRatings",}
    # TODO: Objektivdaten rauskriegen (Namen, Typ, Hersteller und son Käse
    gallery = get_object_or_404(Gallery, pk=gallery_id)
    image = get_object_or_404(GalImage, pk=image_id)

    exifdata = {}
    i = Image.open(image.base_file.file.name)
    inf = i._getexif()
    for tag, value in inf.items():
        decoded = TAGS.get(tag, tag)
        if decoded in allowedTags:
            exifdata[decoded] = value
    
    take_time = exifdata['DateTimeOriginal']    
    try:
        artist = exifdata['Artist']
    except Exception:
        artist = 'unknown'
    try:
        flash = exifdata['Flash']
    except Exception:
        flash = 'unknown'
    try:
        copyright = exifdata['Copyright']
    except Exception:
        copyright = 'unknown'
    try:    
        software = exifdata['Software']
    except Exception:
        software = 'unknown'
    try:
        exposure_time = exifdata['ExposureTime']
    except Exception:
        exposure_time = 'unknown'
    try:    
        focal_length = exifdata['FocalLength']
    except Exception:
        focal_length = 'unknown'
    try:
        make = exifdata['Make']
    except Exception:
        make = 'unknown'
    try:
        model = exifdata['Model']
    except Exception:
        model = 'unknown'
    try:
        fl35 = exifdata['FocalLengthIn35mmFilm']
    except Exception:
        fl35 = 'unknown'
    try:
        iso = exifdata['ISOSpeedRatings']
    except Exception:
        iso = 'unknown'


    context = {'gallery': gallery,
        'image': image,
        'taketime': take_time,
        'artist': artist,
        'flash': flash,
        'copyright': copyright,
        'software': software,
        'exposure_time': exposure_time[0] / exposure_time[1],
        'focal_length': focal_length[0] / focal_length[1],
        'make': make,
        'model': model,
        'fl35': fl35,
        'iso': iso,
        }
    return render(request, 'core/gallery.phtml', context)

