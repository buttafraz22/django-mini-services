# urls.py
from django.urls import path
from .views import *


urlpatterns = [
    # path('generate_invoice', MYVIEW, name='generate_invoice'),
    path('product/add-product', AddProductsView.as_view(), name='add_products'),
    path('product/order', ProcessOrderView.as_view(), name='order-products')
    # Other URL patterns
]
