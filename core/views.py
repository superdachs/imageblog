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

def galleryOverview(request, gallery_id):
    return render(request, 'core/gallery_overview.phtml', context)

def gallery(request, site_id, gallery_id, image_id):
    gallery = get_object_or_404(Gallery, pk=gallery_id)
    image = get_object_or_404(GalImage, pk=image_id)
    lastid = ''
    nextid = ''
    # next image
    count = 0
    for i in gallery.galimages.all():
        currentid = i.id
        if i == image:
            break
        count = count + 1
    try:    
        lastid = (gallery.galimages.all()[count-1].id)
    except Exception:
        lastid = 'none'
    try:
        nextid = (gallery.galimages.all()[count+1].id)
    except Exception:
        nextid == 'none'
    if nextid == '':
        nextid = 'none'

    #############################################################
    # neue metadaten behandlung                                 #
    #############################################################
    cmdline = "exiv2 -pab " + image.base_file.file.name
    p = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    exifdata = {}
    for line in iter(p.stdout.readline, b''):
        try:
            l = re.sub('b\'', '', str(line))
            l = re.sub('\'', '', l)
            l = l.replace("\\n", " ")
            l = re.sub('\s+', ' ', l).strip()
            key = re.sub('\.', '_', l.split( )[0])
            value = l.split(' ', 3 )[3]

            if not value == '(Binary value suppressed)':
                try:
                    urls = re.findall('http[s]?://[0-9a-z./&%$?-]*', value)
                    for url in urls:
                        value = value.replace(url, '<a href="' + url + '">' + url + '</a>')
                except TypeError:
                    pass
                exifdata[key] = value
        except Exception:
            pass
    p.wait()
    #############################################################
       
    # GPS Handling
    if exifdata['Exif_GPSInfo_GPSLatitude']:
        latitudeString = exifdata['Exif_GPSInfo_GPSLatitude']
        longitudeString = exifdata['Exif_GPSInfo_GPSLongitude']
        latitudeRefString = exifdata['Exif_GPSInfo_GPSLatitudeRef']
        longitudeRefString = exifdata['Exif_GPSInfo_GPSLongitudeRef']
        latitudeString = latitudeString.replace('deg ', '°')
        longitudeString = longitudeString.replace('deg ', '°')

    if exifdata['Exif_GPSInfo_GPSAltitude']:
        altitudeString = exifdata['Exif_GPSInfo_GPSAltitude']

# Exif.GPSInfo.GPSVersionID       Byte        4  2.3.0.0
# Exif.GPSInfo.GPSLatitudeRef     Ascii       2  North
# Exif.GPSInfo.GPSLatitude        Rational    3  51deg 2.52500' 
# Exif.GPSInfo.GPSLongitudeRef    Ascii       2  East
# Exif.GPSInfo.GPSLongitude       Rational    3  13deg 48.38460' 
# Exif.GPSInfo.GPSAltitudeRef     Byte        1  Above sea level
# Exif.GPSInfo.GPSAltitude        Rational    1  115 m
# Exif.GPSInfo.GPSTimeStamp       Rational    3  17:43:51
# Exif.GPSInfo.GPSSatellites      Ascii       3  07
# Exif.GPSInfo.GPSDateStamp       Ascii      11  2014:04:06


    context = {'gallery': gallery,
        'image'   : image,
        'exif'    : exifdata,
        'last'    : lastid,
        'next'    : nextid,
        'latstr'  : latitudeString,
        'lonstr'  : longitudeString,
        'latref'  : latitudeRefString,
        'lonref'  : longitudeRefString,
        'altstr'  : altitudeString,
        }
    return render(request, 'core/gallery.phtml', context)



