from django.views.generic.base import TemplateView

from django.core.paginator import Paginator

from .models import Product, ProductCategory


class HomePage(TemplateView):
    """Класс представления главной страницы"""
    template_name = 'index.html'


class ProductsList(TemplateView):
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
