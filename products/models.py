from django.db import models

from users.models import CustomUser


class ProductCategory(models.Model):
    """
    Модель таблицы Категории товаров.
    Поля:
        Название
        Описание
    """
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
    """
    Модель таблицы Товары
    Поля:
        Название
        Изображение
        Описание
        Цена
        Количество
        Категория
    """
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


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)
    
    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    """
    Модель таблицы Корзина товаров.
    Поля:
        Пользователь (многие ко многим)
        Товар (могие ко многим)
        Количество
    """
    user = models.ForeignKey(
        to=CustomUser,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        to=Product,
        verbose_name='Товар',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
    )

    objects = BasketQuerySet.as_manager()

    class Meta:
        verbose_name = 'Карзина'
        verbose_name_plural = 'Позиции в корзине'
    
    def __str__(self):
        return f'{self.user.username}|{self.product.name} {self.quantity} шт.'

    def sum(self):
        """
        Вычисление итоговой суммы за товары
        Цена товара x Количество товара 
        """
        return self.product.price * self.quantity

    def create_or_update(product_id, user):
        """
        Если элемент корзины есть, то обновляет, если нет то создает
        """
        baskets = Basket.objects.filter(user=user, product_id=product_id)

        if not baskets.exists():
            obj = Basket.objects.create(
                user=user,
                product_id=product_id,
                quantity=1
            )
            is_created = True
            return obj, is_created
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
            is_crated = False
            return basket, is_crated
