from django.conf import settings
from django_mako_plus import view_function
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from catalog import models as amod
from django import forms
import requests
from formlib.form import FormMixIn
from .. import dmp_render, dmp_render_to_string

@view_function
@login_required(login_url='/account/login/')
def process_request(request):

    form = ShippingAddressForm(request, initial={
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,})

    if form.is_valid():
        form.commit(request)
        return HttpResponseRedirect('/catalog/checkout/')

    context = {
        'form': form,
    }

    return dmp_render(request, 'shippingaddress.html', context )

class ShippingAddressForm(FormMixIn, forms.Form):
    form_id = 'shipping_address_form'
    def init(self):
        self.fields['first_name'] = forms.CharField(label="First Name")
        self.fields['last_name'] = forms.CharField(label="Last Name")
        self.fields['address'] = forms.CharField(label="Address")
        self.fields['city'] = forms.CharField(label="City")
        self.fields['state'] = forms.CharField(label="State")
        self.fields['zipcode'] = forms.CharField(label="Zipcode")

    def clean(self):
        self.data = self.data.copy()
        address = self.cleaned_data.get('address')
        city = self.cleaned_data.get('city')
        state = self.cleaned_data.get('state')
        zipcode = self.cleaned_data.get('zipcode')

        data = address + ' ' + city + ', ' + state + ' ' + zipcode

        params = {'address': data, 'key': settings.GOOGLE_API_KEY}

        url = 'https://maps.googleapis.com/maps/api/geocode/json'

        response = requests.get(url, params)

        response = response.json()

        if response['status'] != 'OK':
            raise forms.ValidationError("Your address isn't a valid address")

        google_apt = ''
        google_street = ''
        google_route = ''
        google_city = ''
        google_state = ''
        google_zipcode = ''

        for t in response['results'][0]['address_components']:
            if 'subpremise' in t['types']:
                google_apt = t['long_name']
                google_apt = ' #' + google_apt
            if 'street_number' in t['types']:
                google_street = t['long_name']
            if 'route' in t['types']:
                google_route = t['long_name']
            if 'locality' in t['types']:
                google_city = t['long_name']
            if 'administrative_area_level_1' in t['types']:
                google_state = t['long_name']
            if 'postal_code' in t['types']:
                google_zipcode = t['long_name']


        google_address = google_street + ' ' + google_route + google_apt

        if google_address != address or google_city != city or google_state != state or google_zipcode != zipcode:
            self.data['address'] = google_address
            self.data['city'] = google_city
            self.data['state'] = google_state
            self.data['zipcode'] = google_zipcode

            raise forms.ValidationError('Is this corrected address ok? Click submit again if yes, and change it if no')

        return self.cleaned_data



    def commit(self, request):
        shippingaddress = amod.ShippingAddress()
        shippingaddress.user = request.user
        shippingaddress.address = self.cleaned_data.get('address')
        shippingaddress.city = self.cleaned_data.get('city')
        shippingaddress.state = self.cleaned_data.get('state')
        shippingaddress.zipcode = self.cleaned_data.get('zipcode')
        shippingaddress.save()
        return 4
