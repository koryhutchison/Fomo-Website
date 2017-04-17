from django.conf import settings
from django_mako_plus import view_function
from django.http import HttpResponse, HttpResponseRedirect
from catalog import models as cmod
from django import forms
from .. import dmp_render, dmp_render_to_string

@view_function
def process_request(request):

    cart = cmod.ShoppingCart.objects.order_by('create_date').filter(user=request.user)

    context = {
        'cart': cart
    }
    return dmp_render(request, 'shoppingcart.html', context)

@view_function
def delete(request):
    try:
        item = cmod.ShoppingCart.objects.get(id=request.urlparams[0])
    except cmod.ShoppingCart.DoesNotExist:
        return HttpResponseRedirect('/catalog/shoppingcart/')

    item.delete()
    return HttpResponseRedirect('/catalog/shoppingcart/')

@view_function
def clear_cart(request):
    request.user.empty_cart()
    return HttpResponseRedirect('/catalog/shoppingcart/')
