from stock.models import Stock, Category
from django.views.generic import ListView, DetailView
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from comments.forms import CommentAddForm
from comments.models import Comments
from django.contrib import messages


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
# start app comments ###################################################################################################
    form = CommentAddForm

    def post(self, request, **kwargs):
# start like, dislike ##################################################################################################
        like = request.POST.get('like')
        dislike = request.POST.get('dislike')
        return_url = request.POST.get('return_url')
        if like:
            product = Stock.objects.get(id=like)
            if product.likes.filter(id=request.user.id):
                product.likes.remove(request.user.id)
            else:
                product.likes.add(request.user.id)
            return redirect(return_url)
        if dislike:
            product = Stock.objects.get(id=dislike)
            if product.dislikes.filter(id=request.user.id):
                product.dislikes.remove(request.user.id)
            else:
                product.dislikes.add(request.user.id)
            return redirect(return_url)
# end like, dislike ####################################################################################################
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
# end app comments #####################################################################################################

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Просмотр товара'
        context['categories'] = Category.objects.annotate(cnt=Count("stock")).filter(cnt__gt=0)
# start app comments ###################################################################################################
        context['form'] = self.form
        context['comments'] = Comments.objects.all().filter(title=self.object.pk, answer=None, validation=True)
# end app comments #####################################################################################################
# start like, dislike ##################################################################################################
        product = Stock.objects.get(id=self.object.pk)
        if product.likes.filter(id=self.request.user.id):
            context['is_liked'] = True
        else:
            context['is_liked'] = False
        if product.dislikes.filter(id=self.request.user.id):
            context['is_disliked'] = True
        else:
            context['is_disliked'] = False
        context['total_likes'] = product.likes.all()
        context['total_dislikes'] = product.dislikes.all()
# end like, dislike ####################################################################################################
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
