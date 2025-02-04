from django.shortcuts import render
from django.views.generic.base import TemplateView

from django.core.paginator import Paginator

from .models import Product, ProductCategory

class HomePage(TemplateView):
    template_name = 'index.html'


class ProductsList(TemplateView):
    template_name = 'products/products.html'
    per_page = 1

    def get_context_data(self, **kwargs):
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
