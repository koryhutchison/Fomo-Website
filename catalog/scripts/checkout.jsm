<%! from django.conf import settings %>
$(function() {

    var handler = StripeCheckout.configure({
    key: '${settings.STRIPE_API_PUBLIC_KEY}',
    image: 'https://stripe.com/img/documentation/checkout/marketplace.png',
    locale: 'auto',
    token: function(token) {
      // You can access the token ID with `token.id`.
      // Get the token ID to your server-side code for use.
      $('#id_stripe_token').val(token.id);
      $('#checkout_form').submit();
    }
  });

  $('#checkout_form').submit(function(e) {
    // Open Checkout with further options:
    if ($('#id_stripe_token').val() != ''){
      return;
    }
    handler.open({
      name: 'FOMO',
      description: 'Merchandise',
      zipCode: true,
      amount: ${ request.user.calculate_total_with_shipping() } * 100,
    });
    e.preventDefault();
  });

  // Close Checkout on page navigation:
  window.addEventListener('popstate', function() {
    handler.close();
  });

  $('#submit-btn').removeClass('btn-primary').addClass('btn-success')

});
