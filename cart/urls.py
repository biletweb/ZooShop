from django.urls import path
from cart.views import CartList, CartAddRemove

urlpatterns = [
    path('', CartList.as_view(), name="cart_list"),
    path('add/', CartAddRemove.as_view(), name="cart_add_remove"),
]
