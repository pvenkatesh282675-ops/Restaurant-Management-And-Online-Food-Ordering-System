from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    VEG = 'veg'
    NON_VEG = 'nonveg'

    FOOD_TYPE_CHOICES = [
        (VEG, 'Vegetarian'),
        (NON_VEG, 'Non Vegetarian'),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="foods"
    )
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to="foods/", blank=True, null=True)
    food_type = models.CharField(
        max_length=10,
        choices=FOOD_TYPE_CHOICES,
        default=VEG
    )
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name