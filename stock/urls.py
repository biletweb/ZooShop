from django.urls import path
from stock.views import ProductList, CategoryDetail, ProductDetail, SearchList

urlpatterns = [
    path('', ProductList.as_view(), name='stock_list'),
    path('category/<slug:slug>/', CategoryDetail.as_view(), name='stock_category'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='stock_detail'),
    path('search/', SearchList.as_view(), name='stock_search'),
]
