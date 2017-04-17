$(function() {

  $('#cart-badge').attr('data-badge', '${ request.user.get_cart_count() }')

  $('#buy_now_form').ajaxForm({
    target: '#purchase-container',
  });

  // $('#submit-btn').click(function() {
  //   var name = $('#product-name').html();
  //   alert(name + " was added to the cart.");
  // });

});//ready
