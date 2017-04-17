from django.conf import settings
from django_mako_plus import view_function
from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required
from catalog import models as cmod
from account import models as amod
from .. import dmp_render, dmp_render_to_string

@view_function
@login_required
def process_request(request):
    products = cmod.Product.objects.order_by('-price')
    categories = cmod.Category.objects.order_by('name').all()

    last5products = request.user.get_last5()


    context = {
        'products': products,
        'categories': categories,
        'last5products': last5products,
    }
    return dmp_render(request, 'index.html', context)

@view_function
def filter(request):
    category = cmod.Category.objects.get(name=request.urlparams[0])
    products = cmod.Product.objects.filter(category=category)
    categories = cmod.Category.objects.order_by('name').all()
    last5products = request.user.get_last5()


    context = {
        'products': products,
        'categories': categories,
        'last5products': last5products,
    }
    return dmp_render(request, 'index.html', context)
