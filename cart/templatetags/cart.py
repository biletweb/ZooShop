from django import template

register = template.Library()


# проверка продукта на наличие в корзине
@register.filter(name='is_in_cart')
def is_in_cart(products, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == products.id:
            return True
    return False


# подсчет количества текущего товара в корзине
@register.filter(name='item_count')
def item_count(products, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == products.id:
            return round(cart.get(id), 2)
    return 0


# подсчет сумы текущего товара с учетом его количества
@register.filter(name='price_total')
def price_total(product, cart):
    return round(product.sale_price * item_count(product, cart), 2)


# подсчет общей сумы товаров с учетом их количества
@register.filter(name='final_total')
def final_total(products, cart):
    sum = 0
    for p in products:
        sum += price_total(p, cart)
    return round(sum, 2)


# подсчет сумы профита с учетом количества текущего товара
@register.filter(name='profit')
def profit(product, cart):
    sale_price = product.sale_price * item_count(product, cart)
    purchase_price = product.purchase_price * item_count(product, cart)
    profit = sale_price - purchase_price
    return round(profit, 2)


# подсчет общей сумы профита с учетом количества всех товаров
@register.filter(name='final_profit')
def final_profit(products, cart):
    sum = 0
    for p in products:
        sum += profit(p, cart)
    return round(sum, 2)


# подсчет общего количества товара в корзине
@register.filter(name='final_count')
def final_count(products, cart):
    sum = 0
    for p in products:
        sum += item_count(p, cart)
    return round(sum, 2)
