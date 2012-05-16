# coding=utf-8

# BASED ON DJANGO-TUPPERWARE: https://bitbucket.org/jiaaro/django-tupperware
try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local
import re
    
from django.conf import settings
from django.contrib.sites.models import Site
from apps.pharmacies.models import Pharmacy

DEFAULT_SITE_ID = 1

_thread_locals = local()
def get_current_site():
    return getattr(_thread_locals, 'site', Site.objects.get(id=DEFAULT_SITE_ID))

def get_current_appname():
    return Pharmacy.objects.filter(site=get_current_site()).values_list('slug', flat=True)[0]

def set_current_site(site):
    setattr(_thread_locals, 'site', site)

class SiteOnFlyDetectionMiddleware(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage."""
    def process_request(self, request):
        folder = re.search('(?<=^/)(?!admin/)\w+', request.path.lower())
        if folder:
            try:
                current_site = Pharmacy.objects.get(slug=folder.group(0)).site
            except:
                current_site = Site.objects.get(id=DEFAULT_SITE_ID)
        else:
            current_site = Site.objects.get(id=DEFAULT_SITE_ID)
        set_current_site(current_site)
        
        
        
