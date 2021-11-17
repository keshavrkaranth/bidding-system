from django.db.models import Max
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from . import models
from . import serializers
from datetime import datetime, timedelta
from django.utils import timezone


@api_view(['GET'])
def test(request):
    return Response("ok", status=status.HTTP_200_OK)


@api_view(['POST'])
def register_bidder(request):
    data = request.data
    email = data.get('email')
    if not email:
        return Response({'success': False, 'data': 'email id is required'}, status=status.HTTP_400_BAD_REQUEST)
    if not data.get('password'):
        return Response({'success': False, 'data': 'email id is required'}, status=status.HTTP_400_BAD_REQUEST)
    if models.User.objects.filter(email=email).exists():
        return Response({'success': False, 'data': 'email id Already exists'}, status=status.HTTP_400_BAD_REQUEST)
    username = email.split('@')[0]
    user = models.User.objects.create(username=username, email=email)
    user.set_password(data.get('password'))
    user.save()
    return Response({'success': True, 'data': f"Account created note your username:{username}"},
                    status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_product(request):
    data = request.data
    try:
        product = models.Product.objects.create(name=data.get('product_name'), price=data.get('product_price'))
        serializer = serializers.ProductsSerializer(product, many=False)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
    except:
        product = None
    return Response({'success': False, 'data': 'Unable to create product'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_auction(request):
    data = request.data
    if not data.get('username'):
        return Response({'success': False, 'data': 'Username is required'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        user = User.objects.get(username=data['username'])
    except:
        return Response({'success': False, 'data': 'Invalid User'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = models.Product.objects.create(name=data['product_name'], price=data['product_price'])
    except:
        return Response({'success': False, 'data': 'Unable to create product'}, status=status.HTTP_400_BAD_REQUEST)
    ends_at = datetime.now() + timedelta(hours=1)

    try:
        auction = models.Auction.objects.create(hosted_by=user,
                                                product=product,
                                                starting_price=data['starting_price'],
                                                ends_at=ends_at)
        auction.save()

        serializer = serializers.AuctionSerializer(auction)

        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
    except:
        return Response({'success': False, 'data': 'Unable to create auction'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def place_bid(request):
    data = request.data

    bid_price = data.get('bid_price')
    try:
        auction = models.Auction.objects.get(uid=data.get('uid'))
    except:
        return Response({'success': False, 'data': 'Invalid Auction id'})

    if models.Bidder.objects.filter(auction=auction, price=bid_price).exists():
        return Response(
            {'success': False, 'data': 'A user already made bid with same price please bid with more price'},
            status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=data.get('username'))
    except:
        return Response({'success': False, 'data': 'Invalid User'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.get(username=data['username'])
    if models.Bidder.objects.filter(user=user, auction=auction).exists():
        return Response({'success': False, 'data': 'Bid to this auction  already made'},
                        status=status.HTTP_400_BAD_REQUEST)

    if not timezone.now() < auction.ends_at:
        return Response({'success': False, 'data': 'Sorry bid time has expired'}, status=status.HTTP_401_UNAUTHORIZED)

    if not data.get('username'):
        return Response({'success': False, 'data': 'Username is required'}, status=status.HTTP_401_UNAUTHORIZED)

    if not bid_price:
        return Response({'success': False, 'data': 'Bid price is required'}, status=status.HTTP_401_UNAUTHORIZED)

    if bid_price < auction.starting_price:
        return Response({'success': False, 'data': 'Bid price less than auction price'},
                        status=status.HTTP_401_UNAUTHORIZED)

    bid = models.Bidder.objects.create(user=user, auction=auction, price=bid_price)
    bid.save()
    return Response({'success': True, 'data': "Bid successfully placed"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_bid_details(request):
    auction_id = request.query_params.get('auction_id')

    try:
        auction = models.Auction.objects.get(uid=auction_id)
        max_bidder = models.Bidder.objects.filter(auction=auction).aggregate(Max('price'))
        max_price = max_bidder.get('price__max')
        user_id = models.Bidder.objects.get(auction=auction, price=max_bidder.get('price__max')).id
        data = {user_id: max_price}

        return Response({'success': True, 'data': data}, status=status.HTTP_200_OK)

    except:
        return Response({'success': False, 'data': "Invalid auction Id"}, status=status.HTTP_404_NOT_FOUND)
