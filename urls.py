# coding=utf-8

from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from apps.main import admin
from apps.pharmacies.models import Pharmacy


urlpatterns = []

for p in Pharmacy.objects.filter(is_active=True).exclude(site__isnull=True, slug=''):
    admin_farmafiel = admin.FarmaAdminSite(p.slug)
    admin_farmafiel.disable_action('delete_selected')

    urlpatterns += patterns('',(r'^%s/' % p.slug, include(admin_farmafiel.urls, app_name=p.slug,)),)

urlpatterns += patterns('',
    # Examples:
    # url(r'^$', 'farmafiel.views.home', name='home'),
    # url(r'^farmafiel/', include('farmafiel.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    #(r'', include('profiles.urls')),
)

# THIS IS TO SERVE STATIC FILES IN DEVELOPMENT, ONLY WORKS WITH DEBUG=True

urlpatterns += staticfiles_urlpatterns()
