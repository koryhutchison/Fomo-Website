$(function(){
  $('.delete_link').click(function(event) {
    // cancel the default behavior
    event.preventDefault();

    // Open the modal
    $('#deleteConfirm').modal({
      // no options
    });

    var href = $(this).attr('href');

    $('#really-delete-link').attr('href', href);
  });

  $('.update-quantity-button').click(function() {
    var button = $(this);
    var url = "/manager/products.get_quantity/" + button.attr('data-pid');

    // call ajax
    button.siblings('.quantity-text').load(url);
  });

});
