from django.shortcuts import render, HttpResponse
from geopy.geocoders import Nominatim
from aggregator.models import Studioentry
from django.http import JsonResponse
from django.core import serializers


### DJANGO REST

# import django_filters
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import generics
# from rest_framework import mixins
# from rest_framework import viewsets
# from rest_framework import filters
# from rest_framework import permissions
# from rest_framework import metadata
# from rest_framework.views import APIView
# from rest_framework.decorators import detail_route, list_route
# from rest_framework.parsers import FileUploadParser
#from .models import Studioentry
#from .serializers import StudioentrySerializer
#from aggregator.permissions import IsOwnerOrReadOnly

# class StudioentryViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows products to be viewed or edited.
#     """
#     metadata_class = metadata.SimpleMetadata
#     queryset = Studioentry.objects.all()
#     serializer_class = StudioentrySerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrReadOnly,)
#     ordering = ('-created', 'id')
#     #filter_fields = ('price', 'owner', 'category', 'address')
#     #filter_class = ProductFilter
#     search_fields = ('title', 'content')
#     #def get_queryset(self):
#     #    return []
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)





def index(request):
	return render(request, 'index.html', {})

def search(request):

	


	distance = 1
	latitude = request.GET.get('lat','') or 0
	longitude = request.GET.get('lon','') or 0
	if request.GET.get('dist',''):
		distance = request.GET.get('dist','')
	location = {}
	if request.GET.get('address'):
		geolocator = Nominatim()
		location = geolocator.geocode(request.GET.get('address'))
		print "geopy: ", location
		if location:
			latitude = location.latitude
			longitude = location.longitude
	


	print "parm: ", longitude, latitude, distance

	# lazy daisy easy peazy, mwhahahahaha
	new_sql = "select id, astext(geom), name, address from aggregator_studioentry where st_within(geom, envelope(linestring(point(@lon-@dist/abs(cos(radians(@lat))*69), @lat-(@dist/69)), point(@lon+@dist/abs(cos(radians(@lat))*69), @lat+(@dist/69))))) order by st_distance(point(@lon, @lat), geom) limit 20"
	new_sql = new_sql.replace('@lat', str(latitude) ).replace('@lon', str(longitude) ).replace('@dist', str(distance) )

	studios = []

	if ( request.GET.get('lon','') and request.GET.get('lat','') and request.GET.get('dist','') ) or request.GET.get('address',''):
		studios = Studioentry.objects.raw(new_sql)


	#response = JsonResponse(studios, safe=False)
	print "json: ", studios
	data = serializers.serialize('json', studios)
	response = HttpResponse(data, content_type='application/json')

	# for json result
	if request.GET.get('json'):
		response["Access-Control-Allow-Origin"] = "*"
		return response

	# for html result
	return render(request, 'search.html', { 'studios': studios, 'location': location } )






	#response = render_to_response('app/view.html')  
	#response['X-Content-Security-Policy'] = "allow 'self'"  
	#return response
	




