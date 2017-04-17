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


});
