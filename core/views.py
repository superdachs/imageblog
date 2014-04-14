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
    return site(request, 1)

def site(request, site_id):
    sites = Site.objects.all()
    site = get_object_or_404(Site, pk=site_id)
    articles = Article.objects.filter(site = site_id).order_by('-pub_date')
    galleries = Gallery.objects.filter(site = site_id).order_by('-pub_date')
    context = {'site': site,
        'articles': articles,
        'galleries': galleries,
        'sites': sites,
        }
    return render(request, 'core/site.phtml', context)

def article(request, article_id, site_id):
    article = get_object_or_404(Article, pk=article_id)
    site = get_object_or_404(Site, pk=site_id)
    context = {'article': article,
            'site': site,
        }
    return render(request, 'core/article.phtml', context)

def gallery_overview(request, gallery_id, site_id):
    gallery = get_object_or_404(Gallery, pk=gallery_id)
    site = get_object_or_404(Site, pk=site_id)
    context = {'gallery': gallery,
            'site': site,
    }
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
    cmdline = "exiv2 -pa " + image.base_file.file.name
    p = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    exifdata = {}
    for line in iter(p.stdout.readline, b''):
        try:
            l = re.sub('b\'', '', str(line))
            l = re.sub('b"', '', l)
            l = re.sub('"', '', l)
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
                print(key + " : " + value)
        except Exception:
            pass
    p.wait()
    #############################################################



    # GPS Handling
    try:
        latitudeString = exifdata['Exif_GPSInfo_GPSLatitude']
        longitudeString = exifdata['Exif_GPSInfo_GPSLongitude']
        latitudeRefString = exifdata['Exif_GPSInfo_GPSLatitudeRef']
        longitudeRefString = exifdata['Exif_GPSInfo_GPSLongitudeRef']
        latitudeString = latitudeString.replace('deg ', ' ')
        longitudeString = longitudeString.replace('deg ', ' ')
        latdeg = latitudeString.split()[0]
        lattail = latitudeString.split()[1]
        londeg = longitudeString.split()[0]
        lontail = longitudeString.split()[1]
        lattail = float(lattail) / 60
        lontail = float(lontail) / 60
        googlelat = latdeg + "." + str(lattail).split('.')[1]
        googlelon = londeg + "." + str(lontail).split('.')[1]
    except Exception:
        latitudeString = "unknown"
        latitudeRefString = "unknown"
        longitudeString = "unknown"
        longitudeRefString = "unknown"
        googlelat = ''
        googlelon = ''
        pass
    try:
        if exifdata['Exif_GPSInfo_GPSAltitude']:
            altitudeString = exifdata['Exif_GPSInfo_GPSAltitude']
    except Exception:
        altitudeString = "unknown"
        pass


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
        'googlelat' : googlelat,
        'googlelon' : googlelon,
        }
    return render(request, 'core/gallery.phtml', context)



