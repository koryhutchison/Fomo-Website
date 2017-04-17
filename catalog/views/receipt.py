from django.conf import settings
from django_mako_plus import view_function
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from catalog import models as cmod
from django import forms
from formlib.form import FormMixIn
import stripe
from .. import dmp_render, dmp_render_to_string

@view_function
@login_required(login_url='/account/login/')
def process_request(request):

    try:
        sale = cmod.Sale.objects.get(id=request.urlparams[0])
    except cmod.Sale.DoesNotExist:
        return HttpResponseRedirect('/account/index/')

    saleitems = cmod.SaleItem.objects.filter(sale=sale)

    tax = 0
    for i in saleitems:
        tax += i.taxamount


    context = {
        'sale': sale,
        'saleitems': saleitems,
        'tax': tax
    }
    return dmp_render(request, 'receipt.html', context)
