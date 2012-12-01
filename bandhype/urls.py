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

    # #band model
    # url(r'^insertbandslistens$', 'bands.band.insertbandslistens'),
    # url(r'^insertbandstalks$', 'bands.band.insertbandstalks'),
    # url(r'^insertbands$', 'bands.band.insertbands'),


    #bandcount model
    # url(r'^insertbandslistens$', 'bands.bandcount.insertbandcountslistens'),
    # url(r'^insertbandstalks$', 'bands.bandcount.insertbandcountstalks'),
    # url(r'^insertbands$', 'bands.bandcount.insertbandcounts'),

    # #stateband model
    # url(r'^isblistens$', 'bands.stateband.isblistens'),
    # url(r'^isbtalks$', 'bands.stateband.isbtalks'),
    # url(r'^isb$', 'bands.stateband.isb'),

    # #countyband model

    # url(r'^icblistens$', 'bands.stateband.icblistens'),
    # url(r'^icbtalks$', 'bands.stateband.icbtalks'),
    # url(r'^icb$', 'bands.stateband.icb'),

    # #cityband and city model

    # url(r'citylistens$', 'bands.city.listens'),
    # url(r'citytalks$', 'bands.city.talks'),
    # url(r'citycounts$', 'bands.city.counts'),

    # url(r'^bandhype/', include('bandhype.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
