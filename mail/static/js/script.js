const template_change_cards = document.querySelectorAll('.template_change_card');

template_change_cards.forEach((item,index) => {
    item.addEventListener('click',(e) => {
        if(!e.target.matches('#preview_btn')){
            const changing_template_form = item.querySelector('.change_active_template_form');
            changing_template_form.submit();
        }
    })
})



const uploading_file = document.getElementById('upload_html_file'),
              uploading_file_form = document.getElementById('upload_html_file_form');

        uploading_file.addEventListener('change',() => {
            uploading_file_form.submit();
        })

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