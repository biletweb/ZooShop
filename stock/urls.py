from django.urls import path
from stock.views import ProductList, CategoryDetail

urlpatterns = [
    path('', ProductList.as_view(), name='stock_list'),
    path('category/<slug:slug>/', CategoryDetail.as_view(), name='stock_category'),
]
