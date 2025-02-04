from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        max_length=120,
    )
    description = models.TextField(
        verbose_name='Описание категории',
        max_length=300,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        verbose_name='Название продукта',
        max_length=120,
    )
    image = models.ImageField(
        verbose_name='Фото товара',
        upload_to='products/'
    )
    description = models.TextField(
        verbose_name='Описание товара',
        max_length=500,
        null=True,
        blank=True,
    )
    price = models.DecimalField(
        verbose_name='Цена',
        decimal_places=2,
        max_digits=7,
    )
    quantity = models.IntegerField(
        verbose_name='Количество',
        default=0,
    )
    category = models.ForeignKey(
        to=ProductCategory,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
