function slowScroll(id) {
    var offset = 0;
    $('html, body').animate({
      scrollTop: $(id).offset().top - offset
    }, 1700);
    return false;
};


const delete_all_msg = () => {
  const messages = document.querySelectorAll('.message');
  messages.forEach(item => {
    setTimeout(() => {
      item.remove();
    },5000)
  })

}

$(window).on('load', function () {
  $preloader = $('.load-wrapper'),
    $loader = $preloader.find('.load');
  $loader.fadeOut();
  $preloader.delay(350).fadeOut('slow');
  if(document.querySelectorAll('.message') != null && document.querySelectorAll('.message') != undefined){
    delete_all_msg()
  }
});


     