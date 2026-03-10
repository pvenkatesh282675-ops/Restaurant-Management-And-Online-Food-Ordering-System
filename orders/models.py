from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from menu.models import FoodItem

class Order(models.Model):

    STATUS = [
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('Out', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS, default='Pending')
    is_delivered = models.BooleanField(default=False)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.status == 'Delivered':
            self.is_delivered = True
        else:
            self.is_delivered = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.food.name} (x{self.quantity})"