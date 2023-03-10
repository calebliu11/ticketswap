from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Listing
from .serializers import ListingSerializer
from django.core.exceptions import ValidationError

from datetime import date
from datetime import datetime

# Create your views here.

@api_view(['POST'])
def post_listing(request):
    serializer = ListingSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        updated_datetime = datetime.combine(data['date'], datetime.min.time())
        serializer.save(id=data['id'], event=data['event'], description=data['description'], price=data['price'], date=updated_datetime)
    except ValidationError:
        print(serializer.errors)

    return Response(serializer.initial_data)

class RecentListingsList(APIView):
    def get(self, request, format=None):
        listings = Listing.objects.all()[0:12]
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)

