from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required
from catalog import models as cmod
from django import forms
from .. import dmp_render, dmp_render_to_string
from formlib.form import FormMixIn

@view_function
@login_required
@permission_required('catalog.change_product')
def process_request(request):

    try:
        product = cmod.Product.objects.get(id=request.urlparams[0])
    except cmod.Products.DoesNotExist:
        return HttpResponseRedirect('/manager/products/')

    form = ProductEditForm(request, product=product, initial={
        'name': product.name,
        'category': product.category,
        'price': product.price,
        'description': product.description,
        'quantity': getattr(product, 'quantity', 0),
        'serial_number': getattr(product, 'serial_number', 0)
    })
    if form.is_valid():
        form.commit(product)
        return HttpResponseRedirect('/manager/products/')


    context = {
        'product': product,
        'form' : form,
    }
    return dmp_render(request, 'product.html', context)


class ProductEditForm(FormMixIn, forms.Form):
    form_id = 'edit_product_form'
    def init(self, product):
        self.fields['name'] = forms.CharField(label="Product Name", max_length="100")
        self.fields['category'] = forms.ModelChoiceField(label="Category",
            queryset=cmod.Category.objects.order_by('name').all())
        self.fields['price'] = forms.DecimalField(label="Price")
        self.fields['description'] = forms.CharField(label="Description")
        if hasattr(product, 'quantity'):
            self.fields['quantity'] = forms.DecimalField(label="Quantity")
        if hasattr(product, 'serial_number'):
            self.fields['serial_number'] = forms.CharField(label="Serial Number")

    def commit(self, product):
        product.name = self.cleaned_data.get('name')
        product.category = self.cleaned_data.get('category')
        product.price = self.cleaned_data.get('price')
        product.description = self.cleaned_data.get('description')
        if hasattr(product, 'quantity'):
            product.quantity = self.cleaned_data.get('quantity')
        if hasattr(product, 'serial_number'):
            product.serial_number = self.cleaned_data.get('serial_number')
        product.save()
        return 4

@view_function
@permission_required('catalog.delete_product')
def delete(request):
    try:
        product = cmod.Product.objects.get(id=request.urlparams[0])
    except cmod.Products.DoesNotExist:
        return HttpResponseRedirect('/manager/products/')

    product.delete()
    return HttpResponseRedirect('/manager/products/')
