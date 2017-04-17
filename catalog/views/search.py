from django.conf import settings
from django_mako_plus import view_function
from catalog import models as cmod
from django import forms
from .. import dmp_render, dmp_render_to_string

@view_function
def process_request(request):
    categories = cmod.Category.objects.all()

    product_name = request.GET.get('search')

    last5products = request.user.get_last5()

    search_result = cmod.Product.objects

    if product_name:
        search_result = search_result.filter(name__icontains=product_name)


    context = {
        'categories': categories,
        'search_result': search_result,
        'last5products': last5products,
    }
    return dmp_render(request, 'search.html', context)
