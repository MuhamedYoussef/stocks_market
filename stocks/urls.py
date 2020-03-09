from django.urls import path
from .views import *

urlpatterns = [
    path('', Stocks.as_view(), name='stocks'),
    path('get_stocks', get_stocks, name='get_stocks'),
    path('get_stock_detail', get_stock_detail, name='get_stock_detail'),
]