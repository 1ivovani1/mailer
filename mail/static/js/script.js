const template_change_cards = document.querySelectorAll('.template_change_card');

template_change_cards.forEach((item,index) => {
    item.addEventListener('click',(e) => {
        if(!e.target.matches('#preview_btn')){
            const changing_template_form = item.querySelector('.change_active_template_form');
            changing_template_form.submit();
        }
    })
})

const file_dowload_wrapper = document.querySelector('#upload_html_file_form'),
      filename_hidden = document.querySelector('#dowload_file_name'),
      file_label = file_dowload_wrapper.querySelector('.label'),
      uploading_file = document.getElementById('upload_html_file');

const all_forms = document.querySelectorAll('.sending-form');


      all_forms.forEach(item => {
        const inputs = item.querySelectorAll('input');
        item.addEventListener('submit',(e) => {
          e.preventDefault();
          const data = new FormData(item);
          let body = {};
          data.forEach((val,key) => {
            body[key] = val;
          })
          let csrftoken = getCookie('csrftoken');
          postData(body,csrftoken)
          .then((response)=>{
            console.log(response);
            if (response.status !== 200) {
              throw new Error("I can't connect to the server...")
            }
            
            inputs.forEach(item => item.value = '');
          })
          .catch(error => {
            console.error(error);
            inputs.forEach(item => item.value = '');
            
          })
         })
      })


     function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          let cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = cookies[i].trim();
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
    

      const postData = (body,csrf) => {
        return fetch('/',{
          method:'POST',
          headers:{
            'Content-Type':'application/JSON',
            'X-CSRFToken':csrf
          },
          body:JSON.stringify(body)
        })
      }
      
      


        const all_preview_modals = document.querySelectorAll('.template-preview'),
              all_preview_buttons = document.querySelectorAll('.preview-button');
      
        let all_id = []

        all_preview_buttons.forEach((item,index) => {
          all_id.push(item.dataset.target.slice(18));
        });

        all_preview_modals.forEach((element,index) => {
          element.classList.add(`template-preview-${all_id[index]}`);
        });

        const all_modal_contents = document.querySelectorAll('.template-preview-content');
        all_modal_contents.forEach(content => {
          const value = content.textContent;
          content.innerHTML = value;
        })

        const inputs = document.querySelectorAll('.file-input')

        for (var i = 0, len = inputs.length; i < len; i++) {
          customInput(inputs[i])
        }

        function customInput (el) {
          const fileInput = el.querySelector('[type="file"]')
          const label = el.querySelector('[data-js-label]')
          
          fileInput.onchange =
          fileInput.onmouseout = function () {
            if (!fileInput.value) return
            
            var value = fileInput.value.replace(/^.*[\\\/]/, '')
            el.className += ' -chosen'
            label.innerText = value
            console.log(filename_hidden.value);
            
            if(filename_hidden.value != ''){
              filename_hidden.value = file_label.textContent
              file_dowload_wrapper.submit()
            }

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

        if(document.querySelectorAll('.message') != null){
          
          const messages = document.querySelectorAll('.message');
          messages.forEach(item => {
            setTimeout(() => {
              item.remove();
            },5000)
          })
        }