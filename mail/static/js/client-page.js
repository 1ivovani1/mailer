function slowScroll(id) {
    var offset = 0;
    $('html, body').animate({
      scrollTop: $(id).offset().top - offset
    }, 1700);
    return false;
};
(()=>{

    const all_titles_mobile = document.querySelectorAll('.collapsed'),
          all_contents_mobile = document.querySelectorAll('.panel-body'),
          all_titles_desktop = document.querySelectorAll('.nav-pills .nav-link'),
          all_contents_desktop = document.querySelectorAll('.tab-content .tab-pane')

console.log(all_titles_mobile.length,all_titles_desktop.length);


    window.addEventListener('load',() => {
      all_titles_mobile.forEach((item,index) => {
        item.innerHTML = '<img src="./img/info (1) 1.png" alt="">' + all_titles_desktop[index].textContent
      })

      all_contents_mobile.forEach((item,index) => {
        item.innerHTML = all_contents_desktop[index].textContent
      })
    })

    // const all_img_arr = ['./img/Rectangle11.png','./img/Rectangle12.png','./img/Rectangle13.png'];

    // const left_arrow = document.getElementById('left-arr-work'),
    //       right_arrow = document.getElementById('right-arr-work');

    // const card_changing = document.getElementById('worker_img');

    // let index = 0;

    // right_arrow.addEventListener('click',() => {
    //     index++;
    //     if(index == all_img_arr.length) index = 0
    
    //     card_changing.src = all_img_arr[index]

    // });

    // left_arrow.addEventListener('click',() => {
    //     index--;
    //     if(index == -1) index = all_img_arr.length - 1
    
    //     card_changing.src = all_img_arr[index]

    // });

    const wrapper = document.querySelector('#accordion-two');
  wrapper.addEventListener('click',(e) => {
    e.preventDefault()
    let target = e.target;
    const allHeadings = Array.from(document.querySelectorAll('#accordion-two .panel-heading')),
          allContents = document.querySelectorAll('#accordion-two .collapse');

    if (target.matches('#accordion-two .panel-heading, #accordion-two h4, #accordion-two a')) {
      let index = allHeadings.indexOf(target.closest('#accordion-two .panel-heading'));
      allContents.forEach((item,i) => {
        if (i == index) {
          item.style.display = 'block';
        }else{
        item.style.display = 'none';
        }
      })

    }
  });

})()