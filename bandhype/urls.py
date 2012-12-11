from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'bands.views.home', name='home'),
    url(r'^promoters$', 'bands.views.promoters'),
    url(r'^promoterlistens$', 'bands.views.promoterlistens'),
    url(r'^bands$', 'bands.views.bands'),
    url(r'^bandlistens$', 'bands.views.bandlistens'),

    url(r'^counties$', 'bands.views.counties'),
    url(r'^states$', 'bands.views.states'),
    url(r'^unemployment$', 'bands.views.unemployment'),

    url(r'^countycount$', 'bands.views.countycount'),
    url(r'^getcity$', 'bands.views.getcity'),
    url(r'^statecount$', 'bands.views.statecount'),

    url(r'^countrylisten$', 'bands.views.countrylisten'),
    url(r'^listencity$', 'bands.views.listencity'),
    url(r'^timelisten$', 'bands.views.timelisten'),

    # url(r'^fips$','bands.views.fips'),
    # url(r'^bcc$','bands.views.bcc'),
    # url(r'^bsc$','bands.views.bsc'),
    # url(r'^topstate$', 'bands.views.topstate'),
    # url(r'^state$', 'bands.views.state'),
    
    
)
