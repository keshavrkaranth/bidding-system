from django.urls import path
from . import views
from rest_framework import routers
from . import model_views

router = routers.DefaultRouter()
router.register('users',model_views.UserViewSet)
router.register('auctions',model_views.AuctionViewSet)
router.register('bidder',model_views.BidderViewSet)
router.register('products',model_views.ProductViewSet)


urlpatterns = router.urls + [
    path('getRoutes/',views.getRoutes),
    path('register/',views.register_bidder),
    path('create_auction/',views.create_auction),
    path('place_bid/',views.place_bid),
    path('get_auction_bid_details/',views.get_bid_details),
]