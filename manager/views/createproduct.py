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
@permission_required('catalog.add_product')
def process_request(request):

    form = ProductCreateForm(request)
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/manager/products/')


    context = {
        'form' : form,
    }
    return dmp_render(request, 'createproduct.html', context)


class ProductCreateForm(FormMixIn, forms.Form):
    form_id = 'create_product_form'
    def init(self):
        self.fields['product_type'] = forms.ChoiceField(label="Product Type", choices=
        [
            ['unique', 'Unique Product'],
            ['bulk', 'Bulk Product'],
            ['rental', 'Rental Product'],

        ])
        self.fields['name'] = forms.CharField(label="Product Name", max_length="100")
        self.fields['category'] = forms.ModelChoiceField(label="Category",
            queryset=cmod.Category.objects.order_by('name').all())
        self.fields['price'] = forms.DecimalField(label="Price")
        self.fields['description'] = forms.CharField(label="Description", required=False)
        self.fields['quantity'] = forms.DecimalField(label="Quantity", required=False)
        self.fields['serial_number'] = forms.CharField(label="Serial Number", required=False)

    def commit(self):
        if self.cleaned_data.get('product_type') == 'unique':
            product = cmod.UniqueProduct()
        elif self.cleaned_data.get('product_type') == 'bulk':
            product = cmod.BulkProduct()
        elif self.cleaned_data.get('product_type') == 'rental':
            product = cmod.RentalProduct()

        product.name = self.cleaned_data.get('name')
        product.category = self.cleaned_data.get('category')
        product.price = self.cleaned_data.get('price')
        product.description = self.cleaned_data.get('description')
        if hasattr (product, 'quantity'):
            product.quantity = self.cleaned_data.get('quantity')
        if hasattr (product, 'serial_number'):
            product.serial_number = self.cleaned_data.get('serial_number')
        product.save()
        return 4
