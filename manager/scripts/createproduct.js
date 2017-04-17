// This function checks to see what type of product is being entered in, and hides/shows
// the appropriate fields.
$(function() {
  var producttype = $('#id_product_type');

  producttype.change(function(){
    var value = producttype.val();
    if (value == 'unique' || value == 'rental'){
      $('#id_serial_number').closest('p').show(1000);
      $('#id_quantity').closest('p').hide(1000);
    }else {
      $('#id_serial_number').closest('p').hide(1000);
      $('#id_quantity').closest('p').show(1000);
    }
  });

  producttype.change();
});
