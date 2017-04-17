from django.test import TestCase
from account import models as amod
from datetime import datetime, date

class FomoUserTestCase(TestCase):
    def test_create_a_user(self):
        u1 = amod.FomoUser()
        u1.first_name = 'Mike'
        u1.last_name = 'W.'
        u1.email = 'mike@moster.com'
        u1.username = 'mike'
        u1.set_password('Password1')
        u1.birth_date = date(1994,5,19)
        u1.gender = 'Male'
        # add the other fields
        u1.save()

        u2 = amod.FomoUser.objects.get(id=u1.id)

        self.assertEqual(u2.first_name, 'Mike')
        self.assertEqual(u2.last_name, 'W.')
        self.assertEqual(u2.email, 'mike@moster.com')
        self.assertEqual(u2.username, 'mike')
        self.assertEqual(u2.check_password('Password1'), True)
        self.assertEqual(u2.birth_date, date(1994,5,19))
        self.assertEqual(u2.gender, 'Male')


    def test_change_password(self):
        u1 = amod.FomoUser()
        u1.first_name = 'Mike'
        u1.last_name = 'W.'
        u1.email = 'mike@moster.com'
        u1.username = 'mike'
        u1.set_password('Password1')
        u1.birth_date = date(1994,5,19)
        u1.gender = 'Male'
        # add the other fields
        u1.save()
        u1.set_password('Password2')
        u1.save()

        self.assertEqual(u1.check_password('Password2'), True)
