from django.db import models

class Product(models.Model):
    article = models.CharField('Артикул', max_length=50)
    title = models.CharField('Название', max_length=100)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    vendor = models.CharField('Бренд', max_length=100)
    size = models.CharField('Размер', max_length=50)
    description = models.TextField('Описание')

    image = models.ImageField(
        upload_to='products/',
        verbose_name="Фото"
    )

    def __str__(self):
        return self.title