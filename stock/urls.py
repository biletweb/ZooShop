from django.urls import path
from stock.views import ProductList

urlpatterns = [
    path('', ProductList.as_view(), name='stock_list'),
]
