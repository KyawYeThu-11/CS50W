document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  const textarea = document.querySelector('#compose-body');
  
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Making Compose Tab Distinct
  active_tab(document.querySelector("#compose").style);

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-recipients').disabled = false;
  document.querySelector('#compose-subject').value = '';
  textarea.value = '';

  //resizing textarea
  textarea.style.height = '50px';
  const heightLimit = textarea.style.height;
  textarea.onkeyup = function() {
    textarea.style.height = '';
    textarea.style.height = `${Math.max(textarea.scrollHeight, parseInt(heightLimit))}px`;
  };

  document.querySelector('#compose-form').onsubmit = send_email;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email').style.display = 'none';

  // Making current active tab distinct
  if (mailbox==='inbox')
  { 
     active_tab(document.querySelector("#inbox").style);
  }
  else if (mailbox==='archive')
  {
    active_tab(document.querySelector("#archived").style);
  }
  else{
    active_tab(document.querySelector("#sent").style);   
  }

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  // Show list of emails
  fetch(`/emails/${mailbox}`)
  .then(reponse  => reponse.json())
  .then(emails => {
      console.log(emails);

      //Shows a message if there is no email yet
      if (emails.length === 0)
      {
        const message = document.createElement('p');
        message.innerText = 'There is no email yet.'
        document.querySelector('#emails-view').append(message);
      }

      emails.forEach(email=>{
          const id = email.id;
          const sender = email.sender;
          const subject = email.subject;
          const timestamp = email.timestamp;
          const read = email.read;
          
          const container = document.createElement('div');
          container.className = 'container';
          
          const row = document.createElement('div');
          row.className = 'row';
          row.innerHTML = `<div class="col-3">${sender}</div><div class="col-6">${subject}</div><div id="timestamp" class="col-3">${timestamp}</div>`;
          row.addEventListener('click', () => {
            view_email(id)
          });
                
          container.appendChild(row);
          document.querySelector('#emails-view').append(container);
          
          //if read, change color into grey
          if (read === true){
            row.style.backgroundColor = '#fbfbfb';
          }
      })
  });
}

// sending email
function send_email(){
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  
  fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: `${recipients}`,
          subject: `${subject}`,
          body: `${body}`
      })
    })

  .then(response => response.json())
  .then(result => {
      console.log(result);
  });

  load_mailbox('sent')
  return false;
}  

function view_email(id){

  //Show the email & hide the other views
  document.querySelector('#email').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  //Getting the email using its id
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email =>{
    console.log(email);
    const subject = email.subject;
    const timestamp = email.timestamp;
    const sender = email.sender;
    const recipients = email.recipients;
    const body = email.body;
    const archived = email.archived;
    const user = document.querySelector('#username').innerHTML;
    
    const card_header = document.querySelector('.card-header');
    //Displaying subject
    const for_subject = document.createElement('h4');
    for_subject.innerHTML = `${subject}`;
    card_header.append(for_subject);

    //Displaying archive button only if the tab is inbox or archive
    if (sender !== user){
      const archive_btn = document.createElement('img');
      archive_btn.setAttribute('src', 'static/mail/archive.png')
      archive_btn.className='reply_archive';
      archive_btn.setAttribute("id", "archive");
      archive_btn.setAttribute('data-bs-toggle','tooltip');
      if (archived === false){
        archive_btn.setAttribute('title','Archive');
        archive_value = true;
      }else{
        archive_btn.setAttribute('title','Unarchive');
        archive_value = false;
      }
      archive_btn.addEventListener('click', ()=>{
        archive(email.id, archive_value);
      });
      card_header.append(archive_btn);
    }
    
    //Displaying Reply Button
    const reply = document.createElement('img');
    reply.setAttribute('src', 'static/mail/reply.png');
    reply.className = 'reply_archive';
    reply.setAttribute('data-bs-toggle','tooltip');
    reply.setAttribute('title','Reply');
    card_header.append(reply);

    //Compoing Reply Email
    reply.addEventListener('click', ()=>{
      compose_email();
      const recipients_field = document.querySelector('#compose-recipients');
      const subject_field = document.querySelector('#compose-subject');
      const textarea = document.querySelector('#compose-body');

      recipients_field.value=`${sender}`;
      recipients_field.disabled = true;

      if (!subject.startsWith('Re:')){
        subject_field.value=`Re: ${subject}`;
      }else{
        subject_field.value=`${subject}`;
      }

      textarea.value = `\n---------\nOn ${timestamp} <${sender}> wrote: \n\n${body}`;
      textarea.style.height = `${textarea.scrollHeight}px`;
    });
    
    //displaying timestamp, sender, recipients
    const for_timestamp = document.createElement('small');
    const for_usernames = document.createElement('p');
    for_timestamp.innerHTML = `<br><br> ${timestamp}`;
    for_usernames.innerHTML = `From: ${sender} <br> To: &nbsp; &nbsp; ${recipients}`;
    card_header.append(for_timestamp, for_usernames);

    //displaying body
    //use innerText instead to recognise entities
    document.querySelector('.card-text').innerText = `${body}`;
  })

  //Putting the email as read
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body:JSON.stringify({
      read: true
    })
  })
}

function archive(id, archive_value){
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body:JSON.stringify({
      archived: archive_value
    })
  })

  load_mailbox('inbox');
  window.location.reload();
}

function active_tab(button){
  document.querySelector("#compose").style.backgroundColor = '#fdfdfd';
  document.querySelector("#inbox").style.backgroundColor = '#fdfdfd';
  document.querySelector("#archived").style.backgroundColor = '#fdfdfd';
  document.querySelector("#sent").style.backgroundColor = '#fdfdfd';

  button.backgroundColor = 'aliceblue';
}