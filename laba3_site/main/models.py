from django.db import models

# 1. Справочники (будут пополняться автоматически из админки)
class Category(models.Model):
    name = models.CharField('Категория', max_length=100)
    def __str__(self): return self.name

class Vendor(models.Model):
    name = models.CharField('Бренд', max_length=100)
    def __str__(self): return self.name

class Metal(models.Model):
    name = models.CharField('Металл', max_length=100)
    def __str__(self): return self.name

class Color(models.Model):
    name = models.CharField('Цвет', max_length=100)
    def __str__(self): return self.name

class Size(models.Model):
    name = models.CharField('Размер', max_length=50)
    def __str__(self): return self.name

# 2. Сама модель продукта
class Product(models.Model):
    article = models.CharField('Артикул', max_length=50)
    title = models.CharField('Название', max_length=100)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    description = models.TextField('Описание')
    image = models.ImageField(upload_to='products/', verbose_name="Фото")

    # Связи (ForeignKey). При создании товара вы будете выбирать их из выпадающего списка
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Категория")
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, verbose_name="Бренд")
    metal = models.ForeignKey(Metal, on_delete=models.SET_NULL, null=True, verbose_name="Металл")
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, verbose_name="Цвет")
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, verbose_name="Размер")

    def __str__(self):
        return self.title