$(function() {
  var images = $('.product-picture');
  images.hide();
  var current = 0;
  $(images[0]).show();

    $('#picture-btn-next').click(function() {
      //Hides the current image
      $(images[current]).hide();
      current++;
      //Checks to see if current is longer or equal to the lenth of the list
      if (current >= images.length){
        //If so, it resets current to zero so it will show the image at the beginning of the array.
        current = 0;
      }
      //Shows the next image
      $(images[current]).show();
    });//Click


    $('#picture-btn-previous').click(function() {
      //Hides the current image
      $(images[current]).hide();
      current--;
      //Checks to see if it's at the first image in list
      if (current < 0){
        //If so, it changes the current variable to the last indext of list
        current = images.length - 1;
      }
      //Shows the next image
      $(images[current]).show();
    });//Click

});
