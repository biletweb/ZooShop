from django.urls import path
from .views import ProductList

urlpatterns = [
    path('', ProductList.as_view(), name='stock_list'),
    # path('product/<slug:slug>/', ProductDetail.as_view(), name='stock_detail'),
    # path('category/<slug:slug>/', CategoryDetail.as_view(), name='stock_category'),
    # path('search/', SearchList.as_view(), name='stock_search'),
]
