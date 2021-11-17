from rest_framework import serializers
from . import models
from django.db.models import Max
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username', 'date_joined']


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class AuctionSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.Auction
        fields = '__all__'
        depth = 2




class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bidder
        fields = '__all__'
        depth = 2




