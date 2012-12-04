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
    url(r'^bsc$','bands.views.bsc'),
    url(r'^topstate$', 'bands.views.topstate'),
    url(r'^getfips$', 'bands.views.getfips'),
    url(r'^state$', 'bands.views.state'),
    url(r'^getcity$', 'bands.views.getcity'),

    url(r'^timeband$', 'bands.views.timeband'),
    url(r'^btalks$', 'bands.bandcount.btalks'),
    url(r'^stalks$', 'bands.statecount.stalks'),
    url(r'^ctalks$', 'bands.countycount.ctalks'),
    url(r'citytalks$', 'bands.citycount.citytalks'),
    url(r'cityagg$', 'bands.citycount.cityagg')
)
