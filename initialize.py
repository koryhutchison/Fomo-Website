#!/usr/bin/env python3

from django.core import management
from django.db import connection
from datetime import datetime, date
import os, os.path, sys


# ensure the user really wants to do this
areyousure = input('''
  You are about to drop and recreate the entire database.
  All data are about to be deleted.  Use of this script
  may cause itching, vertigo, dizziness, tingling in
  extremities, loss of balance or coordination, slurred
  speech, temporary zoobie syndrome, longer lines at the
  testing center, changed passwords in Learning Suite, or
  uncertainty about whether to call your professor
  'Brother' or 'Doctor'.

  Please type 'yes' to confirm the data destruction: ''')
if areyousure.lower() != 'yes':
    print()
    print('  Wise choice.')
    sys.exit(1)

# initialize the django environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'fomo.settings'
import django
django.setup()


# drop and recreate the database tables
print()
print('Living on the edge!  Dropping the current database tables.')
with connection.cursor() as cursor:
    cursor.execute("DROP SCHEMA public CASCADE")
    cursor.execute("CREATE SCHEMA public")
    cursor.execute("GRANT ALL ON SCHEMA public TO postgres")
    cursor.execute("GRANT ALL ON SCHEMA public TO public")

# make the migrations and migrate
management.call_command('makemigrations')
management.call_command('migrate')

# Imports for Initializer
from account import models as amod
from catalog import models as cmod
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal

# for p in Permission.objects.all():
#     print(p.codename)

# Create your own permissions
content_type = ContentType.objects.get_for_model(amod.FomoUser)
permission = Permission.objects.create(
    codename='user_edit_user',
    name='The user can edit their own account',
    content_type=content_type,
)
permission2 = Permission.objects.create(
    codename='view_products',
    name='Can View all products',
    content_type=content_type,
)
permission3 = Permission.objects.create(
    codename='view_fomousers',
    name='Can view all users',
    content_type=content_type,
)
permission4 = Permission.objects.create(
    codename='manager_change_password',
    name='This allows a manager to change a users password',
    content_type=content_type,
)

# Create groups
g1 = Group()
g1.name = 'Manager'
g1.save()
g1.permissions.add(Permission.objects.get(codename='add_fomouser'))
g1.permissions.add(Permission.objects.get(codename='change_fomouser'))
g1.permissions.add(Permission.objects.get(codename='delete_fomouser'))
g1.permissions.add(Permission.objects.get(codename='view_fomousers'))
g1.permissions.add(Permission.objects.get(codename='add_bulkproduct'))
g1.permissions.add(Permission.objects.get(codename='change_bulkproduct'))
g1.permissions.add(Permission.objects.get(codename='add_category'))
g1.permissions.add(Permission.objects.get(codename='change_category'))
g1.permissions.add(Permission.objects.get(codename='add_product'))
g1.permissions.add(Permission.objects.get(codename='change_product'))
g1.permissions.add(Permission.objects.get(codename='delete_product'))
g1.permissions.add(Permission.objects.get(codename='add_rentalproduct'))
g1.permissions.add(Permission.objects.get(codename='change_rentalproduct'))
g1.permissions.add(Permission.objects.get(codename='add_uniqueproduct'))
g1.permissions.add(Permission.objects.get(codename='change_uniqueproduct'))
g1.permissions.add(Permission.objects.get(codename='view_products'))
g1.permissions.add(Permission.objects.get(codename='manager_change_password'))


g2 = Group()
g2.name = 'Employee'
g2.save()
g2.permissions.add(Permission.objects.get(codename='add_fomouser'))
g2.permissions.add(Permission.objects.get(codename='change_fomouser'))
g2.permissions.add(Permission.objects.get(codename='view_products'))
g2.permissions.add(Permission.objects.get(codename='view_fomousers'))

g3 = Group()
g3.name = 'Customer'
g3.save()
g3.permissions.add(Permission.objects.get(codename='user_edit_user'))


#This creates 4 user accounts
User1 = amod.FomoUser()
User1.username = 'kory.hutchison'
User1.first_name = 'Kory'
User1.last_name = 'Hutchison'
User1.set_password('Password1')
User1.email = 'kory.hutchison@icloud.com'
User1.birth_date = date(1994,5,19)
User1.gender = 'Male'
User1.is_staff = True
User1.is_admin = True
User1.is_active = True
User1.is_superuser = True
User1.save()
User1.groups.add(g1)


User2 = amod.FomoUser()
User2.username = 'nmarrs'
User2.first_name = 'Nathaniel'
User2.last_name = 'Marrs'
User2.set_password('Password1')
User2.email = 'nathanielmarrs@gmail.com'
User2.birth_date = date(1996,3,28)
User2.gender = 'Male'
User2.is_staff = True
User2.is_admin = True
User2.is_active = True
User2.save()
User2.groups.add(g2)


User3 = amod.FomoUser()
User3.username = 'apratt'
User3.first_name = 'Alex'
User3.last_name = 'Pratt'
User3.set_password('Password1')
User3.email = 'alex.w.pratt@gmail.com'
User3.birth_date = date(1993,5,28)
User3.gender = 'Male'
User3.is_staff = True
User3.is_admin = True
User3.is_active = True
User3.save()
User3.groups.add(g3)


User4 = amod.FomoUser()
User4.username = 'brett'
User4.first_name = 'Brett'
User4.last_name = 'Adamson'
User4.set_password('Password1')
User4.email = 'adamsonb12@gmail.com'
User4.birth_date = date(1993,5,11)
User4.gender = 'Male'
User4.is_staff = True
User4.is_admin = True
User4.is_active = True
User4.save()
User4.groups.add(g3)


# create a category
cat1 = cmod.Category()
cat1.codename = 'kids'
cat1.name = 'Kids Toy Products'
cat1.save()

cat2 = cmod.Category()
cat2.codename = 'string'
cat2.name = 'String Instruments'
cat2.save()

cat3 = cmod.Category()
cat3.codename = 'brass'
cat3.name = 'Brass Instruments'
cat3.save()

cat4 = cmod.Category()
cat4.codename = 'woodwind'
cat4.name = 'Woodwind Instruments'
cat4.save()

cat5 = cmod.Category()
cat5.codename = 'sheetmusic'
cat5.name = 'Sheet Music'
cat5.save()

cat6 = cmod.Category()
cat6.codename = 'accessories'
cat6.name = 'Instrument Accessories'
cat6.save()

# Create the Unique Products
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

f1 = cmod.ProductPicture()
f1.product = p1
f1.path = '/static/catalog/media/productpictures/kazoo.jpg'
f1.save()

f1 = cmod.ProductPicture()
f1.product = p1
f1.path = '/static/catalog/media/productpictures/kazoo2.jpg'
f1.save()


p2 = cmod.UniqueProduct()
p2.serial_number = 'asdfasdf'
p2.name = 'Violin'
p2.category = cat2
p2.price = Decimal('150.00')
p2.description = '''A favorite among Suzuki and other private teachers; Warm and
 round tone, playability, hand-feel and consistency will keep you motivated; This
  outfit includes a case, bow, and rosin; Handmade 1/4 violin; Beautiful and dependable.'''
p2.save()

f2 = cmod.ProductPicture()
f2.product = p2
f2.path = '/static/catalog/media/productpictures/violin.jpg'
f2.save()

f2 = cmod.ProductPicture()
f2.product = p2
f2.path = '/static/catalog/media/productpictures/violin2.jpg'
f2.save()

p3 = cmod.UniqueProduct()
p3.serial_number = 'asdfasdf'
p3.name = 'Cello'
p3.category = cat2
p3.price = Decimal('450.00')
p3.description = '''Cecilio CCO-100 cello is ideal for beginner or student cellist
 featuring a crack-proof spruce top, maple back, neck and sides. This cello is
 outfitted with a padded lightweight carrying soft case with pockets and adjustable
 backpack straps (making it convenient to carry to school or orchestra), a
 Brazilwood bow with unbleached horsehair, cello stand, rosin cake, and an extra
 set of cello strings. Please note that the bridge will not be setup before shipment
 to avoid damage to the cello body during transit. Buy with confidence as it comes with
  a 1 year warranty against any manufacturer's defects.'''
p3.save()

f3 = cmod.ProductPicture()
f3.product = p3
f3.path = '/static/catalog/media/productpictures/cello.jpg'
f3.save()

f3 = cmod.ProductPicture()
f3.product = p3
f3.path = '/static/catalog/media/productpictures/cello2.jpg'
f3.save()

p4 = cmod.UniqueProduct()
p4.serial_number = 'asdfasdf'
p4.name = 'Guitar'
p4.category = cat2
p4.price = Decimal('333.99')
p4.description = '''This top-selling acoustic guitar is the perfect instrument for
 a beginner of any age, or as a second instrument for the seasoned player. From
 its detailed appointments to the bold acoustic tones it projects, the Jasmine S35
 dreadnought guitar is an excellent all around solution for any style of music. This
 finely crafted instrument is backed by a limited lifetime warranty.'''
p4.save()

f4 = cmod.ProductPicture()
f4.product = p4
f4.path = '/static/catalog/media/productpictures/guitar.png'
f4.save()

f4 = cmod.ProductPicture()
f4.product = p4
f4.path = '/static/catalog/media/productpictures/guitar2.jpg'
f4.save()

p5 = cmod.UniqueProduct()
p5.serial_number = 'asdfasdf'
p5.name = 'Tuba'
p5.category = cat3
p5.price = Decimal('2999.99')
p5.description = '''Mendini by Cecilio MEP-L is Bb Euphonium (better known as the
 "mini" tuba or "tenor" tuba) with beautiful gold lacquered finish. Its large bore
  tubing is combined with a 12" upright bell to project its rich sound. The 4 top
  action valves with stainless steel pistons and lightweight design make for the
  ideal choice for the student musician.'''
p5.save()

f5 = cmod.ProductPicture()
f5.product = p5
f5.path = '/static/catalog/media/productpictures/tuba.jpg'
f5.save()

f5 = cmod.ProductPicture()
f5.product = p5
f5.path = '/static/catalog/media/productpictures/tuba2.jpg'
f5.save()

p6 = cmod.UniqueProduct()
p6.serial_number = 'asdfasdf'
p6.name = 'Trumpet'
p6.category = cat3
p6.price = Decimal('400.00')
p6.description = '''Mendini by Cecilio trumpets are ideal for beginner or student
 musicians. This trumpet features a phosphorus copper lead mouth pipe, topped with
 3 comfortable white mother of pearl key inlaid and 3 smooth action valves. Every
 trumpet is play tested at Cecilio’s factory and re-tested at their Los Angeles
 distribution center to ensure that their high quality standards are met. This is
 why thousands of instructors have approved these trumpets. This trumpet package
 includes a plush-lined nylon covered hard shell case, a pair of gloves, a soft
 cleaning cloth, and a bottle of valve oil. Buy with confidence as it comes with
 a 1- year warranty against any manufacturer's defects.'''
p6.save()

f6 = cmod.ProductPicture()
f6.product = p6
f6.path = '/static/catalog/media/productpictures/trumpet.jpg'
f6.save()

f6 = cmod.ProductPicture()
f6.product = p6
f6.path = '/static/catalog/media/productpictures/trumpet2.jpg'
f6.save()

p7 = cmod.UniqueProduct()
p7.serial_number = 'asdfasdf'
p7.name = 'Trombone'
p7.category = cat3
p7.price = Decimal('450.00')
p7.description = '''The Jean Paul TB-400 student Tenor Trombone is the ideal instrument
 for beginning and intermediate Trombone players. It offers a quick response with
 accurate tones that produce a very warm and rich sound. The Jean Paul Tenor Trombone
 features a stunning yellow brass body construction, generous bore, and a light yet balanced
 weight which lessens fatigue while playing. Combined with a robust carrying case for
 easy transportation, the Jean Paul Tenor Trombone makes the perfect choice for new musicians.'''
p7.save()

f7 = cmod.ProductPicture()
f7.product = p7
f7.path = '/static/catalog/media/productpictures/trombone.jpg'
f7.save()

f7 = cmod.ProductPicture()
f7.product = p7
f7.path = '/static/catalog/media/productpictures/trombone2.jpg'
f7.save()

p8 = cmod.UniqueProduct()
p8.serial_number = 'asdfasdf'
p8.name = 'Saxophone'
p8.category = cat4
p8.price = Decimal('649.99')
p8.description = '''The Jean Paul AS-400 Alto Saxophone is the perfect sax for beginning
 and intermediate music students. It offers a superior tone in its class, with even
 key action and placement that feels just right for band members. Its fluid key work
 gives it a relaxed feeling for any saxophonist, while its well-rounded intonation
 and warm sound make it a welcome instrument in any band.'''
p8.save()

f8 = cmod.ProductPicture()
f8.product = p8
f8.path = '/static/catalog/media/productpictures/saxophone.jpg'
f8.save()

f8 = cmod.ProductPicture()
f8.product = p8
f8.path = '/static/catalog/media/productpictures/saxophone2.jpeg'
f8.save()

p9 = cmod.UniqueProduct()
p9.serial_number = 'asdfasdf'
p9.name = 'Clarinet'
p9.category = cat4
p9.price = Decimal('399.99')
p9.description = '''Mendini by Cecilio MCT clarinets are the perfect instrument
for the student musician. This clarinet features high quality body with durable
nickel plated Inline trill keys and adjustable thumb rest. Every clarinet is inspected
by technicians at Cecilio's distribution center in the United States to ensure that
their high quality standards are met.'''
p9.save()

f9 = cmod.ProductPicture()
f9.product = p9
f9.path = '/static/catalog/media/productpictures/clarinet.jpg'
f9.save()

f9 = cmod.ProductPicture()
f9.product = p9
f9.path = '/static/catalog/media/productpictures/clarinet2.jpg'
f9.save()

p10 = cmod.UniqueProduct()
p10.serial_number = 'asdfasdf'
p10.name = 'Flute'
p10.category = cat4
p10.price = Decimal('479.99')
p10.description = '''The Yamaha YFL-222 Standard flute in C features drawn and
curled tone holes, covered keys and an offset G. It has a nickel silver headjoint,
 body and footjoint and a silver-plated finish. I features a C-footjoint and pointed
  key arms, and comes with a Yamaha standard plastic flute case, polishing cloth,
  polishing gauze, cleaning rod and Flute Owner’s Manual.'''
p10.save()

f10 = cmod.ProductPicture()
f10.product = p10
f10.path = '/static/catalog/media/productpictures/flute.jpg'
f10.save()

f10 = cmod.ProductPicture()
f10.product = p10
f10.path = '/static/catalog/media/productpictures/flute2.jpg'
f10.save()

# Create Renal Products
p11 = cmod.RentalProduct()
p11.serial_number = 'rsdfasdf'
p11.name = 'Kazoo - Rental'
p11.category = cat1
p11.price = Decimal('10.00')
p11.description = '''The Grover Trophy Metal Kazoo is a great introduction to music
 and musical instruments. The kazoo features a durable metal body ideal for classroom
 use. The Grover Trophy Metal Kazoo is one of the easiest instruments to learn to
 play and is priced individually. Colors may vary.'''
p11.save()

f11 = cmod.ProductPicture()
f11.product = p11
f11.path = '/static/catalog/media/productpictures/kazoo.jpg'
f11.save()

f11 = cmod.ProductPicture()
f11.product = p11
f11.path = '/static/catalog/media/productpictures/kazoo2.jpg'
f11.save()

p12 = cmod.RentalProduct()
p12.serial_number = 'rsdfasdf'
p12.name = 'Violin - Rental'
p12.category = cat2
p12.price = Decimal('50.00')
p12.description = '''A favorite among Suzuki and other private teachers; Warm and
 round tone, playability, hand-feel and consistency will keep you motivated; This
  outfit includes a case, bow, and rosin; Handmade 1/4 violin; Beautiful and dependable.'''
p12.save()

f12 = cmod.ProductPicture()
f12.product = p12
f12.path = '/static/catalog/media/productpictures/violin.jpg'
f12.save()

f12 = cmod.ProductPicture()
f12.product = p12
f12.path = '/static/catalog/media/productpictures/violin2.jpg'
f12.save()

p13 = cmod.RentalProduct()
p13.serial_number = 'rsdfasdf'
p13.name = 'Cello - Rental'
p13.category = cat2
p13.price = Decimal('100.00')
p13.description = '''Cecilio CCO-100 cello is ideal for beginner or student cellist
 featuring a crack-proof spruce top, maple back, neck and sides. This cello is
 outfitted with a padded lightweight carrying soft case with pockets and adjustable
 backpack straps (making it convenient to carry to school or orchestra), a
 Brazilwood bow with unbleached horsehair, cello stand, rosin cake, and an extra
 set of cello strings. Please note that the bridge will not be setup before shipment
 to avoid damage to the cello body during transit. Buy with confidence as it comes with
  a 1 year warranty against any manufacturer's defects.'''
p13.save()

f13 = cmod.ProductPicture()
f13.product = p13
f13.path = '/static/catalog/media/productpictures/cello.jpg'
f13.save()

f13 = cmod.ProductPicture()
f13.product = p13
f13.path = '/static/catalog/media/productpictures/cello2.jpg'
f13.save()

p14 = cmod.RentalProduct()
p14.serial_number = 'rsdfasdf'
p14.name = 'Guitar - Rental'
p14.category = cat2
p14.price = Decimal('70.00')
p14.description = '''This top-selling acoustic guitar is the perfect instrument for
 a beginner of any age, or as a second instrument for the seasoned player. From
 its detailed appointments to the bold acoustic tones it projects, the Jasmine S35
 dreadnought guitar is an excellent all around solution for any style of music. This
 finely crafted instrument is backed by a limited lifetime warranty.'''
p14.save()

f14 = cmod.ProductPicture()
f14.product = p14
f14.path = '/static/catalog/media/productpictures/guitar.png'
f14.save()

f14 = cmod.ProductPicture()
f14.product = p14
f14.path = '/static/catalog/media/productpictures/guitar2.jpg'
f14.save()

p15 = cmod.RentalProduct()
p15.serial_number = 'rsdfasdf'
p15.name = 'Tuba - Rental'
p15.category = cat3
p15.price = Decimal('200.00')
p15.description = '''Mendini by Cecilio MEP-L is Bb Euphonium (better known as the
 "mini" tuba or "tenor" tuba) with beautiful gold lacquered finish. Its large bore
  tubing is combined with a 12" upright bell to project its rich sound. The 4 top
  action valves with stainless steel pistons and lightweight design make for the
  ideal choice for the student musician.'''
p15.save()

f15 = cmod.ProductPicture()
f15.product = p15
f15.path = '/static/catalog/media/productpictures/tuba.jpg'
f15.save()

f15 = cmod.ProductPicture()
f15.product = p15
f15.path = '/static/catalog/media/productpictures/tuba2.jpg'
f15.save()

p16 = cmod.RentalProduct()
p16.serial_number = 'rsdfasdf'
p16.name = 'Trumpet - Rental'
p16.category = cat3
p16.price = Decimal('60.00')
p16.description = '''Mendini by Cecilio trumpets are ideal for beginner or student
 musicians. This trumpet features a phosphorus copper lead mouth pipe, topped with
 3 comfortable white mother of pearl key inlaid and 3 smooth action valves. Every
 trumpet is play tested at Cecilio’s factory and re-tested at their Los Angeles
 distribution center to ensure that their high quality standards are met. This is
 why thousands of instructors have approved these trumpets. This trumpet package
 includes a plush-lined nylon covered hard shell case, a pair of gloves, a soft
 cleaning cloth, and a bottle of valve oil. Buy with confidence as it comes with
 a 1- year warranty against any manufacturer's defects.'''
p16.save()

f16 = cmod.ProductPicture()
f16.product = p16
f16.path = '/static/catalog/media/productpictures/trumpet.jpg'
f16.save()

f16 = cmod.ProductPicture()
f16.product = p16
f16.path = '/static/catalog/media/productpictures/trumpet2.jpg'
f16.save()

p17 = cmod.RentalProduct()
p17.serial_number = 'rsdfasdf'
p17.name = 'Trombone - Rental'
p17.category = cat3
p17.price = Decimal('80.00')
p17.description = '''The Jean Paul TB-400 student Tenor Trombone is the ideal instrument
 for beginning and intermediate Trombone players. It offers a quick response with
 accurate tones that produce a very warm and rich sound. The Jean Paul Tenor Trombone
 features a stunning yellow brass body construction, generous bore, and a light yet balanced
 weight which lessens fatigue while playing. Combined with a robust carrying case for
 easy transportation, the Jean Paul Tenor Trombone makes the perfect choice for new musicians.'''
p17.save()

f17 = cmod.ProductPicture()
f17.product = p17
f17.path = '/static/catalog/media/productpictures/trombone.jpg'
f17.save()

f17 = cmod.ProductPicture()
f17.product = p17
f17.path = '/static/catalog/media/productpictures/trombone2.jpg'
f17.save()

p18 = cmod.RentalProduct()
p18.serial_number = 'rsdfasdf'
p18.name = 'Saxophone - Rental'
p18.category = cat4
p18.price = Decimal('90.00')
p18.description = '''The Jean Paul AS-400 Alto Saxophone is the perfect sax for beginning
 and intermediate music students. It offers a superior tone in its class, with even
 key action and placement that feels just right for band members. Its fluid key work
 gives it a relaxed feeling for any saxophonist, while its well-rounded intonation
 and warm sound make it a welcome instrument in any band.'''
p18.save()

f18 = cmod.ProductPicture()
f18.product = p18
f18.path = '/static/catalog/media/productpictures/saxophone.jpg'
f18.save()

f18 = cmod.ProductPicture()
f18.product = p18
f18.path = '/static/catalog/media/productpictures/saxophone2.jpeg'
f18.save()

p19 = cmod.RentalProduct()
p19.serial_number = 'rsdfasdf'
p19.name = 'Clarinet - Rental'
p19.category = cat4
p19.price = Decimal('100.00')
p19.description = '''Mendini by Cecilio MCT clarinets are the perfect instrument
for the student musician. This clarinet features high quality body with durable
nickel plated Inline trill keys and adjustable thumb rest. Every clarinet is inspected
by technicians at Cecilio's distribution center in the United States to ensure that
their high quality standards are met.'''
p19.save()

f19 = cmod.ProductPicture()
f19.product = p19
f19.path = '/static/catalog/media/productpictures/clarinet.jpg'
f19.save()

f19 = cmod.ProductPicture()
f19.product = p19
f19.path = '/static/catalog/media/productpictures/clarinet2.jpg'
f19.save()

p20 = cmod.RentalProduct()
p20.serial_number = 'rsdfasdf'
p20.name = 'Flute - Rental'
p20.category = cat4
p20.price = Decimal('110.00')
p20.description = '''The Yamaha YFL-222 Standard flute in C features drawn and
curled tone holes, covered keys and an offset G. It has a nickel silver headjoint,
 body and footjoint and a silver-plated finish. I features a C-footjoint and pointed
  key arms, and comes with a Yamaha standard plastic flute case, polishing cloth,
  polishing gauze, cleaning rod and Flute Owner’s Manual.'''
p20.save()

f20 = cmod.ProductPicture()
f20.product = p20
f20.path = '/static/catalog/media/productpictures/flute.jpg'
f20.save()

f20 = cmod.ProductPicture()
f20.product = p20
f20.path = '/static/catalog/media/productpictures/flute2.jpg'
f20.save()

# Create the Bulk Products
p21 = cmod.BulkProduct()
p21.name = 'Bulk Kazoo'
p21.category = cat1
p21.price = Decimal('9.50')
p21.description = '''The Grover Trophy Metal Kazoo is a great introduction to music
 and musical instruments. The kazoo features a durable metal body ideal for classroom
 use. The Grover Trophy Metal Kazoo is one of the easiest instruments to learn to
 play and is priced individually. Colors may vary.'''
p21.quantity = 20
p21.reorder_trigger = 5
p21.reorder_quantity = 20
p21.save()

f21 = cmod.ProductPicture()
f21.product = p21
f21.path = '/static/catalog/media/productpictures/kazoo.jpg'
f21.save()

f21 = cmod.ProductPicture()
f21.product = p21
f21.path = '/static/catalog/media/productpictures/kazoo2.jpg'
f21.save()

p22 = cmod.BulkProduct()
p22.name = 'Dust in the Wind'
p22.category = cat5
p22.price = Decimal('20.00')
p22.description = '''Considered one of the greatest Kansas songs of all time, Dust
in the Wind is a great piece of music that everyone should learn.'''
p22.quantity = 10
p22.reorder_trigger = 5
p22.reorder_quantity = 20
p22.save()

f22 = cmod.ProductPicture()
f22.product = p22
f22.path = '/static/catalog/media/productpictures/dust.jpg'
f22.save()

f22 = cmod.ProductPicture()
f22.product = p22
f22.path = '/static/catalog/media/productpictures/dust2.jpg'
f22.save()

p23 = cmod.BulkProduct()
p23.name = 'Thriller'
p23.category = cat5
p23.price = Decimal('50.00')
p23.description = '''Arguably Michael Jackson's greatest song ever, Thriller is
one of the classic songs that everyone enjoys.'''
p23.quantity = 15
p23.reorder_trigger = 5
p23.reorder_quantity = 20
p23.save()

f23 = cmod.ProductPicture()
f23.product = p23
f23.path = '/static/catalog/media/productpictures/thriller.jpg'
f23.save()

f23 = cmod.ProductPicture()
f23.product = p23
f23.path = '/static/catalog/media/productpictures/thriller2.jpg'
f23.save()

p24 = cmod.BulkProduct()
p24.name = "Disney's Greatest Hits"
p24.category = cat5
p24.price = Decimal('100.00')
p24.description = '''Who doesn't like Disney? This sheetmusic is something that every
family should have so they can teach their kids to play some of the most beloved
songs in the World.'''
p24.quantity = 6
p24.reorder_trigger = 5
p24.reorder_quantity = 20
p24.save()

f24 = cmod.ProductPicture()
f24.product = p24
f24.path = '/static/catalog/media/productpictures/disney.jpg'
f24.save()

f24 = cmod.ProductPicture()
f24.product = p24
f24.path = '/static/catalog/media/productpictures/disney2.jpg'
f24.save()

p25 = cmod.BulkProduct()
p25.name = 'Reeds (Box of 10)'
p25.category = cat6
p25.price = Decimal('35.00')
p25.description = '''These are high quality reeds that will provide high quality sound
for your instrument.'''
p25.quantity = 20
p25.reorder_trigger = 5
p25.reorder_quantity = 20
p25.save()

f25 = cmod.ProductPicture()
f25.product = p25
f25.path = '/static/catalog/media/productpictures/reeds.jpg'
f25.save()

f25 = cmod.ProductPicture()
f25.product = p25
f25.path = '/static/catalog/media/productpictures/reeds2.png'
f25.save()

p26 = cmod.BulkProduct()
p26.name = 'Acoustic Guitar Strings'
p26.category = cat6
p26.price = Decimal('10.00')
p26.description = '''These are some great guitar strings for those that have jammed
out so hard on their other strings which caused them to brake. So if you are one of those
people, these durable strings are for you!'''
p26.quantity = 13
p26.reorder_trigger = 5
p26.reorder_quantity = 21
p26.save()

f26 = cmod.ProductPicture()
f26.product = p26
f26.path = '/static/catalog/media/productpictures/strings.jpg'
f26.save()

f26 = cmod.ProductPicture()
f26.product = p26
f26.path = '/static/catalog/media/productpictures/strings2.jpg'
f26.save()

addr = cmod.ShippingAddress()
addr.user = User1
addr.address = '298 E 1960 N'
addr.city = 'Orem'
addr.state = 'Utah'
addr.zipcode = '84057'
addr.save()

addr = cmod.ShippingAddress()
addr.user = User2
addr.address = '298 E 1960 N'
addr.city = 'Orem'
addr.state = 'Utah'
addr.zipcode = '84057'
addr.save()

sh1 = cmod.ShoppingCart()
sh1.user = User1
sh1.product = p2
sh1.quantity = 1
sh1.save()

sh2 = cmod.ShoppingCart()
sh2.user = User1
sh2.product = p26
sh2.quantity = 2
sh2.save()

sh3 = cmod.ShoppingCart()
sh3.user = User2
sh3.product = p24
sh3.quantity = 2
sh3.save()

sh4 = cmod.ShoppingCart()
sh4.user = User2
sh4.product = p3
sh4.quantity = 1
sh4.save()

s1 = cmod.Sale.record_sale(User1, [sh1, sh2])
User1.empty_cart()
s2 = cmod.Sale.record_sale(User2, [sh3, sh4])
User2.empty_cart()
