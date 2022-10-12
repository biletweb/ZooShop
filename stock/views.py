from stock.models import Stock, Category
from django.views.generic import ListView, DetailView
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
############################################ start app comments ########################################################
from django.urls import reverse_lazy
from comments.forms import CommentAddForm
from comments.models import Comments
from django.contrib import messages
############################################# end app comments #########################################################


class ProductList(ListView):
    model = Stock  # model for work
    template_name = 'stock/list_product.html'  # default stock_list.html
    context_object_name = 'list_product'  # default object_list
    ordering = ['-added_at']
    paginate_by = 3  # number of posts per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['categories'] = Category.objects.annotate(cnt=Count('stock')).filter(cnt__gt=0)
        return context

    def get_queryset(self):
        return Stock.objects.filter(availability=True)


class CategoryDetail(ListView):
    model = Stock  # model for work
    template_name = 'stock/category_product.html'  # default stock_list.html
    context_object_name = 'category_product'  # default object_list
    ordering = ['-added_at']
    paginate_by = 3  # number of posts per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_category_info = Category.objects.get(slug=self.kwargs['slug'])
        context['title'] = current_category_info.title
        context['categories'] = Category.objects.annotate(cnt=Count('stock')).filter(cnt__gt=0)
        context['current_category_info'] = current_category_info
        return context

    def get_queryset(self):
        category_get = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Stock.objects.filter(category=category_get.pk, availability=True)


class ProductDetail(DetailView):
    model = Stock  # model for work
    template_name = 'stock/detail_product.html'  # default stock_detail.html
    context_object_name = 'detail_product'  # default object
############################################ start app comments ########################################################
    form = CommentAddForm

    def post(self, request, **kwargs):
        form = CommentAddForm(request.POST)
        if form.is_valid():
            title = self.get_object()
            comment_id = request.POST.get('comment_id')
            if comment_id:
                comment_answer = Comments.objects.get(id=comment_id)
            else:
                comment_answer = None
            form.instance.user = request.user
            form.instance.title = title
            form.instance.answer = comment_answer
            form.save()
            messages.success(request, 'Ваш комментарий/ответ был успешно добавлен')
            return redirect(reverse_lazy('stock_detail', kwargs={'slug': title.slug}))
############################################# end app comments #########################################################

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Просмотр товара'
        context['categories'] = Category.objects.annotate(cnt=Count("stock")).filter(cnt__gt=0)
############################################ start app comments ########################################################
        context['form'] = self.form
        context['comments'] = Comments.objects.all().filter(title=self.object.pk, answer=None, validation=True)
############################################# end app comments #########################################################
        return context

    def get_queryset(self):
        return Stock.objects.filter(availability=True)


class SearchList(ListView):
    model = Stock  # model for work
    template_name = 'stock/search_product.html'  # default stock_list.html
    context_object_name = 'search_product'  # default object_list
    ordering = ['-added_at']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поиск товара'
        context['q'] = self.request.GET.get('q')
        context['categories'] = Category.objects.annotate(cnt=Count('stock')).filter(cnt__gt=0)
        return context

    def get_queryset(self):
        if self.request.GET.get('q') == '':
            return Stock.objects.filter(title__icontains='None', availability=True)
        else:
            return Stock.objects.filter(title__icontains=self.request.GET.get('q'), availability=True)
