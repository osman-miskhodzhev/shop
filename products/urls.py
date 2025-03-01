from django.urls import path

from .views import (
    HomePage,
    ProductsList,
    basket_add,
    basket_delete,
)

app_name = 'products'

urlpatterns = [
    path('', HomePage.as_view(), name='homepage'),
    path('products/', ProductsList.as_view(), name='products-list'),
    path(
        'products/page/<int:page>/',
        ProductsList.as_view(),
        name='products-page'
    ),
    path(
        'category/<int:category_id>/',
        ProductsList.as_view(),
        name='category-filter'
    ),
    path(
        'basket/add/<int:product_id>/',
        basket_add,
        name='basket-add'
    ),
    path(
        'basket/delete/<int:basket_id>/',
        basket_delete,
        name='basket-delete'
    ),
]
