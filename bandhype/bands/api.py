# from django.contrib.auth.models import User
# from tastypie import fields
# from tastypie.resources import ModelResource
# from bands.models import CountyBand, County


# class CountyResource(ModelResource):
#     class Meta:
#         queryset = County.objects.all()
#         resource_name = 'county'


# class CountyBandResource(ModelResource):
#     county = fields.ForeignKey(CountyResource, 'county')

#     class Meta:
#         queryset = CountyBand.objects.all()
#         resource_name = 'countyband'

#         