import uuid

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Product_name:{self.name}-->Price:{self.price}"


class Auction(models.Model):
    hosted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uid = models.UUIDField(default=uuid.uuid4(), editable=False, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    starting_price = models.FloatField()
    ends_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Product:{self.product}-->uuid{self.uid}-->ends_at:{self.ends_at}"


class Bidder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, models.CASCADE)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"user:{self.user}-->product:{self.auction}-->price:{self.price}"
