from rest_framework import viewsets
from . import models
from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    pagination_class = None


class AuctionViewSet(viewsets.ModelViewSet):
    queryset = models.Auction.objects.all()
    serializer_class = serializers.AuctionSerializer
    pagination_class = None


class BidderViewSet(viewsets.ModelViewSet):
    queryset = models.Bidder.objects.all()
    serializer_class = serializers.BidSerializer
    pagination_class = None


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductsSerializer
    pagination_class = None
