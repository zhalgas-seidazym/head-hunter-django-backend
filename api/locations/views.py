from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import CountrySerializer, CitySerializer

@extend_schema(tags=["Locations"])
class CountryListView(generics.ListAPIView):
    serializer_class = CountrySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

@extend_schema(tags=["Locations"])
class CityListView(generics.ListAPIView):
    serializer_class = CitySerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['country']
