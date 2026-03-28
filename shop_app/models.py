from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    seller = models.ForeignKey(User, on_delete=models.CASCADE) # Standart User
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE) # Standart User
    quantity = models.PositiveIntegerField(default=1)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='Kutilmoqda')
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ('Kutilmoqda', 'Kutilmoqda'),
        ('Yetkazildi', 'Topshirildi'),  # Bu yerda 'Yetkazildi' bazada saqlanadi, 'Topshirildi' ko'rinadi
        ('Bekor qilindi', 'Bekor qilindi'),
    )



class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
