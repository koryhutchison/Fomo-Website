from django.db import models
from django.contrib.auth.models import AbstractUser
from catalog import models as cmod
from decimal import Decimal

GENDER_CHOICES = [
    ['male', 'Male'],
    ['female', 'Female'],
    ['other', 'Other'],
]

class FomoUser(AbstractUser):
    # username
    # first_name
    # last_name
    # password
    # email
    # last_login
        ###The above and more are fields that are already generated and inherited
        ###from the classes
    address = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    zipcode = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.TextField(null=True, blank=True, choices=GENDER_CHOICES)

    def empty_cart(self):
        try:
            cart = cmod.ShoppingCart.objects.filter(user_id=self.id)
            cart.delete()
        except cmod.ShoppingCart.DoesNotExist:
            return False
        return True

    def get_cart_items(self):
        try:
            cart = cmod.ShoppingCart.objects.filter(user_id=self.id)
        except cmod.ShoppingCart.DoesNotExist:
            return False
        return cart

    def get_last5(self):
        history = cmod.History.objects.filter(user_id=self.id).order_by('-create_date')
        distinct_products = []
        for h in history:
            if h.product in distinct_products:
                pass
            else:
                distinct_products.append(h.product)

        last5 = distinct_products[:5]

        return last5

    def get_cart_count(self):
        count = cmod.ShoppingCart.objects.filter(user_id=self.id).count()
        return count

    def get_cart_subtotal(self):
        amount = 0
        items = cmod.ShoppingCart.objects.filter(user=self)
        for i in items:
            amount += i.get_extended_amount()
        return amount

    def calculate_tax(self):
        tax = Decimal(self.get_cart_subtotal()) * Decimal(.0725)
        tax = round(tax, 2)
        return tax

    def calculate_total(self):
        total = self.calculate_tax() + self.get_cart_subtotal()
        return total

    def calculate_total_with_shipping(self):
        total = self.calculate_total() + 10
        return total
