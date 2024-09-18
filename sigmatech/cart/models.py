from django.db import models
from django.conf import settings
from product.models import Product  # Ensure this import is correct based on your project structure

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart of {self.user}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())
    
    def save(self, *args, **kwargs):
        if self.active:
            # Deactivate all other carts for this user
            Cart.objects.filter(user=self.user, active=True).exclude(id=self.id).update(active=False)
        super().save(*args, **kwargs)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else 'Unknown Product'}"

    def total_price(self):
        return self.quantity * (self.product.price if self.product else 0)
