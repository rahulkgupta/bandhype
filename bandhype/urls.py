from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'bands.views.home', name='home'),
    url(r'^promoters$', 'bands.views.promoters'),
    url(r'^bands$', 'bands.views.bands'),
    url(r'^counties$', 'bands.views.counties'),
    url(r'^states$', 'bands.views.states'),
    url(r'^unemployment$', 'bands.views.unemployment'),
    url(r'^countrypop$', 'bands.views.countrypop'),
    url(r'^fips$','bands.views.fips'),
    url(r'^bcc$','bands.views.bcc'),
    url(r'^getfips$', 'bands.views.getfips')
    # url(r'^bandhype/', include('bandhype.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
