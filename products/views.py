from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect

from .models import Product, ProductCategory, Basket
from core.views import CommonTemplateMixin

class HomePage(CommonTemplateMixin, TemplateView):
    """Класс представления главной страницы"""
    template_name = 'index.html'
    title = 'Store'


class ProductsList(CommonTemplateMixin, TemplateView):
    """
    Клас представления страницы товаров
    Если в параметрах указана категория товара, товары фильтрутся по этой
    категории. Если категория товара не указана, то передаются все товары

    Возвращяет контекст со следующим содержимым:
        Товары
        Категории

    Для отображения товаров используется пагинация, на одной странице
    максимум 12 товаров
    """
    template_name = 'products/products.html'
    title = 'Каталог'
    per_page = 12

    def get_context_data(self, **kwargs):
        """
        Метод формирования контекста.
        Логика пагинации расположена здесь.
        """
        context = super().get_context_data(**kwargs)
        context['product_categories'] = ProductCategory.objects.all()

        if 'category_id' in kwargs:
            category = ProductCategory.objects.get(id=kwargs['category_id'])
            products = Product.objects.filter(category=category)
            context['category_id'] = category
        else:
            products = Product.objects.all()

        if 'page' in kwargs:
            page = kwargs['page']
        else:
            page = 1

        paginator = Paginator(products, self.per_page)
        products_paginator = paginator.get_page(page)

        context['products'] = products_paginator
        return context


@login_required
def basket_add(request, product_id):
    Basket.create_or_update(product_id, request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def basket_delete(request, basket_id):
    Basket.objects.get(id=basket_id).delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
