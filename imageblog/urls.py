from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
import os.path

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'imageblog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^sites/', include('core.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
