from django.test import TestCase
from catalog import models as cmod
from datetime import datetime, date
from decimal import Decimal

class ProductTestCase(TestCase):
    def test_create_a_user(self):
        cat1 = cmod.Category()
        cat1.codename = 'kids'
        cat1.name = 'Kids Toy Products'
        cat1.save()

        p1 = cmod.UniqueProduct()
        p1.serial_number = 'asdfasdf'
        p1.name = 'Kazoo'
        p1.category = cat1
        p1.price = Decimal('99.50')
        p1.description = '''The Grover Trophy Metal Kazoo is a great introduction to music
         and musical instruments. The kazoo features a durable metal body ideal for classroom
         use. The Grover Trophy Metal Kazoo is one of the easiest instruments to learn to
         play and is priced individually. Colors may vary.'''
        p1.save()

        p2 = cmod.Product.objects.get(id=p1.id)

        self.assertEqual(p2.serial_number, 'asdfasdf')
        self.assertEqual(p2.name, 'Kazoo')
        self.assertEqual(p2.category.codename, 'kids')
        self.assertEqual(p2.price, Decimal('99.50'))
        self.assertEqual(p2.description, '''The Grover Trophy Metal Kazoo is a great introduction to music
         and musical instruments. The kazoo features a durable metal body ideal for classroom
         use. The Grover Trophy Metal Kazoo is one of the easiest instruments to learn to
         play and is priced individually. Colors may vary.''')

    def test_delete_product(self):
        cat1 = cmod.Category()
        cat1.codename = 'kids'
        cat1.name = 'Kids Toy Products'
        cat1.save()

        p1 = cmod.UniqueProduct()
        p1.serial_number = 'asdfasdf'
        p1.name = 'Kazoo'
        p1.category = cat1
        p1.price = Decimal('99.50')
        p1.description = '''The Grover Trophy Metal Kazoo is a great introduction to music
         and musical instruments. The kazoo features a durable metal body ideal for classroom
         use. The Grover Trophy Metal Kazoo is one of the easiest instruments to learn to
         play and is priced individually. Colors may vary.'''
        p1.save()

        p2 = cmod.Product.objects.get(id=p1.id)

        self.assertEqual(p2.name, 'Kazoo')

        p2.delete()

        try:
            # Checks to see if there is a product, and if the query works, it raises an error
            p3 = cmod.Product.objects.get(id=p1.id)
            raise ValueError
        except cmod.Product.DoesNotExist:
            # This is if the delete worked
            print('>>>>', 'Delete Worked')
