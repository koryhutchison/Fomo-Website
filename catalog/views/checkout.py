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

    cart = cmod.ShoppingCart.objects.order_by('create_date').filter(user=request.user)

    form = CheckoutForm(request)
    if form.is_valid():
        saleid = form.commit(cart)
        url = '/catalog/receipt/' + str(saleid) + '/'
        return HttpResponseRedirect(url)

    context = {
        'form': form,
        'cart': cart
    }
    return dmp_render(request, 'checkout.html', context)

class CheckoutForm(FormMixIn, forms.Form):
    form_id = 'checkout_form'
    form_submit = 'Pay Now'
    def init(self):
        self.fields['stripe_token'] = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean(self):
        stripe.api_key = settings.STRIPE_API_KEY
        try:
            stripe.Charge.create(
                  amount=int(self.request.user.calculate_total_with_shipping() * 100),
                  currency="usd",
                  description="Merchandise",
                  source=self.cleaned_data.get('stripe_token'),
                )
        except stripe.error.CardError as e:
          # Since it's a decline, stripe.error.CardError will be caught
          body = e.json_body
          err  = body['error']

          print("Status is: %s" % e.http_status)
          print("Type is: %s" % err['type'])
          print("Code is: %s" % err['code'])
          # param is '' in this case
          print("Param is: %s" % err['param'])
          print("Message is: %s" % err['message'])
        except stripe.error.RateLimitError as e:
          # Too many requests made to the API too quickly
          raise forms.ValidationError('Too many requests made too quickly')
        except stripe.error.InvalidRequestError as e:
          # Invalid parameters were supplied to Stripe's API
          raise forms.ValidationError('Please try again, or reach out to site admin')
        except stripe.error.AuthenticationError as e:
          # Authentication with Stripe's API failed
          # (maybe you changed API keys recently)
          raise forms.ValidationError('Please contact site admin')
        except stripe.error.APIConnectionError as e:
          # Network communication with Stripe failed
          raise forms.ValidationError('No network communication')
        except stripe.error.StripeError as e:
          # Display a very generic error to the user, and maybe send
          # yourself an email
          raise forms.ValidationError('There was an error, please try again.')
        except Exception as e:
          # Something else happened, completely unrelated to Stripe
          raise forms.ValidationError('There was an error, please try again.')

        return self.cleaned_data

    def commit(self, cart):
        sale = cmod.Sale.record_sale(self.request.user, cart)

        if sale:
            self.request.user.empty_cart()

        return sale
