from django.db import models
from django.contrib.auth.models import User
from main.models import Product

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Новые поля из checkout
    last_name = models.CharField('Фамилия', max_length=50, blank=True)
    first_name = models.CharField('Имя', max_length=50, blank=True)
    middle_name = models.CharField('Отчество', max_length=50, blank=True)
    region = models.CharField('Область', max_length=100, blank=True)
    postal_code = models.CharField('Почтовый индекс', max_length=20, blank=True)
    address = models.CharField('Адрес', max_length=255, blank=True)
    
    # Старые поля
    phone = models.CharField('Телефон', max_length=20, blank=True)
    city = models.CharField('Город', max_length=100, blank=True)
    bio = models.TextField('О себе', max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"Профиль {self.user.username}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Корзина {self.user.username}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.title} ({self.quantity} шт.)"

    @property
    def total_price(self):
        return self.product.price * self.quantity

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Код {self.code} для {self.user.username}"

class PasswordResetCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Сброс пароля для {self.user.username}"

class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email')
    address = models.CharField('Адрес', max_length=255)
    city = models.CharField('Город', max_length=100)
    postal_code = models.CharField('Индекс', max_length=20)
    region = models.CharField('Область', max_length=100, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    total_price = models.DecimalField('Общая сумма', max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Заказ №{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество', default=1)

    def __str__(self):
        return f"{self.product.title if self.product else 'Товар удален'} ({self.quantity} шт.)"

    @property
    def total_price(self):
        return self.price * self.quantity