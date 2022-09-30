from stock.models import Stock, Category
from django.views.generic import ListView
from django.db.models import Count


class ProductList(ListView):
    model = Stock  # модель с которой нужно будет работать
    template_name = 'stock/list_product.html'  # по умолчанию sklad_list.html
    context_object_name = 'stock'  # по умолчанию objects_list
    ordering = ['-added_at']
    paginate_by = 3  # сколько записей будет выводиться на странице

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['categories'] = Category.objects.annotate(cnt=Count("stock")).filter(cnt__gt=0)
        #                                          start cart
        # context['cart_count'] = Stock.objects.filter(availability=True)
        #                                           end cart
        return context

    def get_queryset(self):
        return Stock.objects.filter(availability=True)
