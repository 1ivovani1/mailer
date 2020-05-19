const template_change_cards = document.querySelectorAll('.template_change_card');

template_change_cards.forEach((item,index) => {
    item.addEventListener('click',(e) => {
        if(!e.target.matches('#preview_btn')){
            const changing_template_form = item.querySelector('.change_active_template_form');
            changing_template_form.submit();
        }
    })
})

window.addEventListener('DOMContentLoaded',()=> {
  let sent = document.getElementById('sent_mails'),
      unsent = document.getElementById('unsent_mails'),
      parsed = document.getElementById('parsed'),
      unparsed = document.getElementById('unparsed');

      
var ctx2 = document.getElementById('parsing_statistics').getContext('2d');
var myChart2 = new Chart(ctx2, {
    type: 'pie',
    data: {
        labels: ['Не распарсились', 'Распарсились'],
        datasets: [{
            label: 'Parsing',
            data: [Number(unparsed.textContent), Number(parsed.textContent)],
            backgroundColor: [
              'rgba(255, 206, 86, 0.5)',
              'rgba(153, 102, 255, 0.5)',
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(75, 192, 192, 1)',
            ],
            borderWidth: 0
        }]
    },
    options: {
        responsive:true,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});


var ctx1 = document.getElementById('email_statistics').getContext('2d');
var myChart1 = new Chart(ctx1, {
    type: 'pie',
    data: {
        labels: ['Неотправленные', 'Отправленные'],
        datasets: [{
            label: 'Emails',
            data: [Number(unsent.textContent), Number(sent.textContent)],
            backgroundColor: [
                'rgba(255, 99, 132, 0.5)',
                'rgba(75, 192, 192, 0.5)'
            ],
            borderColor: [
                'rgba(230, 230, 230, 1)',
                'rgba(230, 230, 230, 1)',
            ],
            borderWidth: 0
        }]
    },
    options: {
        responsive:true,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});


})

const email_txt_input_text = document.getElementById('email_txt_text'),
      hidden_input_text = document.getElementById('email_txt_filename_text'),
      email_txt_label_text = document.getElementById('email_txt_label_text');

email_txt_input_text.addEventListener('change',() => {
    setTimeout(() => {
      const filename = email_txt_label_text.textContent;
      hidden_input_text.value = filename.substr(filename.length - 3);
    },1000) 
})
 

const email_txt_input = document.getElementById('email_txt'),
      hidden_input = document.getElementById('email_txt_filename'),
      email_txt_label = document.getElementById('email_txt_label');

email_txt_input.addEventListener('change',() => {
    setTimeout(() => {
      const filename = email_txt_label.textContent;
      hidden_input.value = filename.substr(filename.length - 3);
    },1000) 
})

const html_txt_input = document.getElementById('upload_html_file'),
      hidden_html_input = document.getElementById('dowload_file_name'),
      html_label = document.getElementById('html_download_label');

html_txt_input.addEventListener('change',() => {
    setTimeout(() => {
      const filename = html_label.textContent;
      hidden_html_input.value = filename;
      
      
    },1000) 
})


const mailRuBtn = document.getElementById('mail_ru'),
      gmailComBtn = document.getElementById('gmail_com');
  
const sendingForm = document.querySelector('.sending-form'),
      host = document.querySelector('.host'),
      port = document.querySelector('.port'),
      is_ssl = document.querySelector('.use_ssl'),
      is_tls = document.querySelector('.use_tls');

mailRuBtn.addEventListener('click',() => {
    host.value = 'smtp.mail.ru';
    port.value = 465;
    is_ssl.checked = true;
    is_tls.checked = false;
})

gmailComBtn.addEventListener('click',() => {
  host.value = 'smtp.gmail.com';
  port.value = 587;
  is_ssl.checked = false;
  is_tls.checked = true;
})



    const inputs = document.querySelectorAll('.file-input')

    for (var i = 0, len = inputs.length; i < len; i++) {
      customInput(inputs[i])
    }

    const file_dowload_wrapper = document.getElementById('upload_html_file_form'),
    uploading_file = document.getElementById('upload_html_file');

  uploading_file.addEventListener('change',() => {
    setTimeout(()=> {
      file_dowload_wrapper.submit()
    },1200)
  })


    function customInput (el) {
      const fileInput = el.querySelector('[type="file"]')
      const label = el.querySelector('[data-js-label]')
      
      fileInput.onchange =
      fileInput.onmouseout = function () {
        if (!fileInput.value) return
        
        var value = fileInput.value.replace(/^.*[\\\/]/, '')
        el.className += ' -chosen'
        label.innerText = value
        
        
        

      }
    }

    const mail_password = document.getElementById('mail-password'),
          pass_length = mail_password.dataset.password.length,
          eye = document.getElementById('eye');

    let dots = '';
    for(let i = 0;i<pass_length;i++){
      dots += '•'  
    }
    mail_password.textContent = dots;
    
    eye.addEventListener('click',() => {
        if(mail_password.textContent == dots)
          mail_password.textContent = mail_password.dataset.password
        else
          mail_password.textContent = dots
    })



    const delete_all_msg = () => {
      const messages = document.querySelectorAll('.message');
      messages.forEach(item => {
        setTimeout(() => {
          item.remove();
        },5000)
      })
    
  }

    window.addEventListener('load',() => {
      if(document.querySelectorAll('.message') != null && document.querySelectorAll('.message') != undefined){
        delete_all_msg()
      }
    })


  