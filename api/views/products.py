from django.conf import settings
from django_mako_plus import view_function
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from datetime import datetime
from catalog import models as cmod
from .. import dmp_render, dmp_render_to_string
import json

@view_function
def process_request(request):
    product_name = None
    min_price = None
    max_price = None
    category_name = None

    if request.GET.get('name'):
        product_name = request.GET.get('name')
    if request.GET.get('min'):
        min_price = request.GET.get('min')
    if request.GET.get('max'):
        max_price = request.GET.get('max')
    if request.GET.get('catname'):
        category_name = request.GET.get('catname')
    if product_name == min_price == max_price == category_name == None:
        return HttpResponseNotFound('Bad query')

    product_list = []

    products = cmod.Product.objects

    if product_name:
        products = products.filter(name__icontains=product_name)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if category_name:
        products = products.filter(category__name__icontains=category_name)

    if products.exists():
        for p in products:
            if hasattr(p, 'serial_number'):
                ret = {
                    'name': p.name,
                    'serial_number': p.serial_number,
                    'category': p.category.name,
                    'price': p.price,
                    'description': p.description,
                }
            if hasattr(p, 'quantity'):
                ret = {
                    'name': p.name,
                    'category': p.category.name,
                    'price': p.price,
                    'description': p.description,
                    'quantity': p.quantity,
                    'reorder_trigger': p.reorder_trigger,
                    'reorder_quantity': p.reorder_quantity,
                }

            product_list.append(ret)
    else:
        return HttpResponseNotFound('Bad query')




    return JsonResponse(product_list, safe=False)
