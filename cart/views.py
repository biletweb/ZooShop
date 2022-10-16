import uuid
from django.shortcuts import render, redirect
from django.db.models import Count
from django.views.generic import ListView
from cart.models import Orders, Products
from stock.models import Stock, Category
from django.contrib import messages


# функция добавляет/удаляет весовой товар в корзину из списка товаров
class CartAddRemove(ListView):
    def post(self, request):
        product_id = request.POST.getlist('product_id')
        product_name = request.POST.getlist('product_name')
        product_amount = request.POST.getlist('product_amount')
        product_price_purchase = request.POST.getlist('product_price_purchase')
        product_price_sale = request.POST.getlist('product_price_sale')
        product_price = request.POST.getlist('product_price')
        product_profit = request.POST.getlist('product_profit')
        product_price_total = request.POST.get('product_price_total')
        product_profit_total = request.POST.get('product_profit_total')
        phone = request.POST.get('phone')
        order = uuid.uuid4()

        if product_id:
            for i in range(len(product_id)):
                print('id:', product_id[i],
                      'Товар:', product_name[i],
                      'Кол:', product_amount[i],
                      'Цена закупки:', product_price_purchase[i],
                      'Цена продажи:', product_price_sale[i],
                      'Итого цена:', product_price[i],
                      'Итого профит:', product_profit[i])
                if not Orders.objects.filter(order=order):
                    Orders.objects.create(order=order,
                                          user=self.request.user,
                                          phone=phone,
                                          price_total=product_price_total,
                                          profit_total=product_profit_total)
                    order_id = Orders.objects.get(order=order)
                Products.objects.create(product=product_name[i],
                                        order=order_id,
                                        amount=product_amount[i],
                                        price=product_price[i],
                                        profit=product_profit[i])
            del request.session['cart']
            messages.success(request, 'Ваш заказ успешно оформлен, менеджер с вами скоро свяжется')
            return redirect('cart_list')
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        # amount = request.POST.get('amount')  # функция добавление развесного товара вместо штучного
        cart = request.session.get('cart')
        return_url = request.POST.get('return_url')  # ссылка на возврат страницы заказа товара
        if cart:
            qty = cart.get(product)
            if qty:
                if remove:
                    if qty <= 1:
                    # if qty <= float(amount):
                        cart.pop(product)
                    else:
                        cart[product] = qty - 1
                        # cart[product] = qty - float(amount)
                else:
                    cart[product] = qty + 1
                    # cart[product] = qty + float(amount)
            else:
                cart[product] = 1
                # cart[product] = float(amount)
        else:
            cart = {}
            cart[product] = 1
            # cart[product] = float(amount)
        request.session['cart'] = cart
        # return redirect('stock_list')
        return redirect(return_url)


# функция отображает все товары в корзине и удаляет полностью товар с нее
class CartList(ListView):
    def get(self, request):
        cart = request.session.get('cart')
        delete = self.request.GET.get('delete')
        if delete:
            if delete in cart:
                cart.pop(delete)
                request.session['cart'] = cart
            else:
                messages.error(request, f'Ошибка удаления, такого товара в корзине нет')
        if not cart:
            request.session['cart'] = {}
        id = list(request.session.get('cart').keys())
        prods = Stock.objects.filter(id__in=id, availability=True)
        context = {
            'title': 'Корзина',
            'categories': Category.objects.annotate(cnt=Count("stock")).filter(cnt__gt=0),
            'prods': prods,
            'cart_count': Stock.objects.filter(availability=True)
        }
        return render(request, 'cart/cart.html', context)
