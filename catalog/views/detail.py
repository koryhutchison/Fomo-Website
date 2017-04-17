from django.conf import settings
from django_mako_plus import view_function
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django import forms
from formlib.form import FormMixIn
from catalog import models as cmod
from .. import dmp_render, dmp_render_to_string

@view_function
def process_request(request):


    try:
        product = cmod.Product.objects.get(id=request.urlparams[0])
    except cmod.Product.DoesNotExist:
        return HttpResponseRedirect('/catalog/index/')


    last5products = request.user.get_last5()

    # Add products to the History table
    hprod = cmod.History()
    hprod.product = product
    hprod.user = request.user
    hprod.save()

    form = Buy_Form(request, product=product, initial={'form_product': product.id,})
    if form.is_valid():
        form.commit(request, product)


    template_name = 'detail.html'
    if request.method == 'POST':
        template_name = 'detail-ajax.html'

    return dmp_render(request, template_name, { 'product': product, 'last5products': last5products, 'form': form,})

class Buy_Form(FormMixIn, forms.Form):
    form_id = 'buy_now_form'
    form_submit = 'Buy Now'
    def init(self, product):
        self.fields['form_product'] = forms.CharField(widget=forms.HiddenInput())
        if hasattr(product, 'quantity'):
            self.fields['quantity'] = forms.IntegerField(label='Quantity', required=False)

    def clean(self):
        try:
            product = cmod.Product.objects.get(id=self.request.urlparams[0])
        except cmod.Product.DoesNotExist:
            raise forms.ValidationError("That Product is out of Stock")
            
        if hasattr(product, 'quantity'):
            qty = self.cleaned_data.get('quantity')
            if qty > product.quantity:
                raise forms.ValidationError("Too large of quantity")
        try:
            cart_product = cmod.ShoppingCart.objects.get(product=product)
        except cmod.ShoppingCart.DoesNotExist:
            return self.cleaned_data

        if cart_product.product_id:
            if hasattr(product, 'quantity'):
                pass
            else:
                raise forms.ValidationError("Item already in Cart")

        return self.cleaned_data


    def commit(self, request, product):
        try:
            cart_item = cmod.ShoppingCart.objects.filter(user=request.user).get(product=product)
            cart_item.quantity = cart_item.quantity + self.cleaned_data.get('quantity')
            cart_item.save()
        except:
            cart = cmod.ShoppingCart()
            cart.user = request.user
            cart.product = product
            if hasattr(product, 'quantity'):
                cart.quantity = self.cleaned_data.get('quantity')
            cart.save()

        return 4



@view_function
def modal(request):
    try:
        pictures = cmod.ProductPicture.objects.filter(product__id=request.urlparams[0])
    except cmod.ProductPicture.DoesNotExist:
        return HttpResponseRedirect('/catalog/detail/')



    return dmp_render(request, 'detail.modal.html', {'pictures': pictures})
