from stock.models import Stock, Category
from django.views.generic import ListView
from django.db.models import Count


class ProductList(ListView):
    model = Stock  # model for work
    template_name = 'stock/list_product.html'  # default sklad_list.html
    context_object_name = 'stock'  # default objects_list
    ordering = ['-added_at']
    paginate_by = 3  # number of posts per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['categories'] = Category.objects.annotate(cnt=Count("stock")).filter(cnt__gt=0)
        return context

    def get_queryset(self):
        return Stock.objects.filter(availability=True)
