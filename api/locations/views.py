from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.filters import SearchFilter

from .models import City, Country
from .serializers import CountrySerializer, CitySerializer


@extend_schema(tags=["Locations"])
class CountryListView(generics.ListAPIView):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['name']

@extend_schema(tags=["Locations"])
class CityListView(generics.ListAPIView):
    serializer_class = CitySerializer
    filter_backends = [SearchFilter]
    queryset = City.objects.all()
    search_fields = ['name']
