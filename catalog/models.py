from django.db import models
from polymorphic.models import PolymorphicModel
from account import models as amod
from decimal import Decimal

# Create your models here.

class Category(models.Model):
    # id
    codename = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(PolymorphicModel):
    # id
    name = models.TextField(blank=True, null=True)
    # Always put it on the many side
    category = models.ForeignKey('Category')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

class ProductPicture(models.Model):
    product = models.ForeignKey('Product', related_name='pictures')
    path = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.path


class BulkProduct(Product):
    # id
    # name
    # catagory
    # price
    # create_date
    # modified_date
    # product = models.OneToOneField('Product')
    quantity = models.IntegerField(blank=True, null=True)
    reorder_trigger = models.IntegerField(blank=True, null=True)
    reorder_quantity = models.IntegerField(blank=True, null=True)

class UniqueProduct(Product):
    # id
    # name
    # catagory
    # price
    # create_date
    # modified_date
    serial_number = models.TextField()
    available = models.BooleanField(default=True)

class RentalProduct(Product):
    # id
    # name
    # catagory
    # price
    # create_date
    # modified_date
    serial_number = models.TextField()
    available = models.BooleanField(default=True)


class Sale(models.Model):
    #id
    user = models.ForeignKey('account.FomoUser', related_name='sales')
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    shipping = models.DecimalField(max_digits=8, decimal_places=2, default=10)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)

    @staticmethod
    def record_sale(user, cart_items_list):
        # Create a record_sale() method in your models.py file.  This method should
        shippingaddress = ShippingAddress.objects.filter(user=user).order_by('-create_date').first()

        try:
            # 1) create a Sale object,
            sale = Sale()
            sale.user = user
            sale.shipping = 10
            sale.subtotal = user.get_cart_subtotal()
            sale.total = user.calculate_total_with_shipping()
            sale.save()

            shippingaddress.sale = sale
            shippingaddress.save()

            # 2) create one or more SaleItem objects for the purchases,
            for item in cart_items_list:
                saleitem = SaleItem()
                saleitem.sale = sale
                saleitem.product = item.product
                saleitem.taxrate = .0725
                saleitem.taxamount = Decimal(saleitem.taxrate) * Decimal(item.product.price) * Decimal(item.quantity)
                saleitem.quantity = item.quantity
                saleitem.save()

                # 5) update BulkProduct quantities and IndividualProduct availability.
                if hasattr(item.product, 'quantity'):
                    item.product.quantity -= item.quantity
                    item.product.save()
                if hasattr(item.product, 'available'):
                    item.product.available = False
                    item.product.save()

            # 4) create a Payment object,
            payment = Payments()
            payment.sale = sale
            payment.amount = sale.total
            payment.save()

        except BaseException:
            return False

        return sale.id



class SaleItem(models.Model):
    #id
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE, related_name='sale')
    product = models.ForeignKey('Product', related_name='saleitems')
    taxrate = models.DecimalField(max_digits=8, decimal_places=4, default=.0725)
    taxamount = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def get_extended_amount(self):
        return Decimal(self.quantity * self.product.price)

class Payments(models.Model):
    #id
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE, related_name='payments')
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class History(models.Model):
    #id
    user = models.ForeignKey('account.FomoUser', on_delete=models.CASCADE, related_name='user')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='products')
    create_date = models.DateTimeField(auto_now_add=True)

class ShoppingCart(models.Model):
    #id
    user = models.ForeignKey('account.FomoUser', on_delete=models.CASCADE, related_name='shoppingcart')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product')
    quantity = models.IntegerField(default=1)
    create_date = models.DateTimeField(auto_now_add=True)

    def get_extended_amount(self):
        return Decimal(self.quantity * self.product.price)

class ShippingAddress(models.Model):
    user = models.ForeignKey('account.FomoUser')
    sale = models.ForeignKey('Sale', related_name='shippingaddress', null=True, blank=True)
    address = models.TextField(blank=True)
    city = models.TextField(blank=True)
    state = models.TextField(blank=True)
    zipcode = models.TextField(blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
