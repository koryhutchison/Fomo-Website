$(function() {

  $('#picture-modal').click(function() {
      $.loadmodal('/catalog/detail.modal/${product.id}/');
  });

  $('#buy_now_form').ajaxForm({
    target: '#purchase-container',
  });

  // $('#submit-btn').click(function() {
  //   var name = $('#product-name').html();
  //   alert(name + " was added to the cart.")
  // });

});//ready
