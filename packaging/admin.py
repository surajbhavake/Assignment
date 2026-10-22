
# Register your models here.
from django.contrib import admin
from .models import Product, ShippingBox, Order, OrderItem

admin.site.register(Product)
admin.site.register(ShippingBox)
admin.site.register(Order)
admin.site.register(OrderItem)