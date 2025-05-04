let currentLanguage = getBrowserLanguage() || 'en';

function getBrowserLanguage() {
  // Versuche, die bevorzugte Sprache des Browsers zu erhalten
  let browserLanguage = navigator.language || navigator.userLanguage;

  if (
    browserLanguage &&
    (browserLanguage === 'de' || browserLanguage.startsWith('de-'))
  ) {
    return 'de';
  } else {
    return 'en';
  }
}
// Function to change the language
/*
function changeLanguage(lang) {
    currentLanguage = lang;
    loadContentContact();
}
*/

//receive form data from opem.html
function sendOpenContact() {
  let openData = document.getElementById('textfeld').value;
  console.log('Saving selection:', openData, typeof openData);
  fetch('/save-selection-open', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ Data: openData }),
  })
    .then((response) => {
      console.log('Server response: ', response);
      return response.json();
    })
    .then((sel_data) => console.log(sel_data))
    .catch((err) => console.error(err));
}

function submitOpenData() {
  sendOpenData();
  fetch('/data', {
    method: 'GET',
  });
}

function checkTextfeld() {
  let textfeldWert = document.getElementById('textfeld').value.trim();
  if (textfeldWert === '') {
    handleEmptyFieldError();
    return false;
  } else {
    return 'en';
  }
}

function handleEmptyFieldError() {
  fetch('language/contact_language-data.json')
    .then((response) => response.json())
    .then((data) => {
      const fehlerText = data[currentLanguage].emptyFieldError;
      alert(fehlerText);
    })
    .catch((error) =>
      console.error('Error loading language data file:', error),
    );
}

// Function to load content based on the selected language
function loadContentContact() {
  console.log('Loading content (contact) for language:', currentLanguage);
  fetch('language/contact_language-data.json')
    .then((response) => response.json())
    .then((data) => {
      const navbarData = data[currentLanguage].navbar;
      const GreyboxData = data[currentLanguage].Greybox;
      updateContent(navbarData);
      updateGreybox(GreyboxData);
    })
    .catch((error) =>
      console.error('Error loading language data file:', error),
    );
}

// Function to update the Introduction content on the page
function updateContent(data) {
  document.getElementById('nav-home').innerText = data.home;
  document.getElementById('nav-about').innerText = data.about;
  document.getElementById('nav-contact').innerText = data.contact;
}

// Function to update the greybox content on the page
function updateGreybox(data) {
  document.getElementById('send_us').innerHTML = data.send_us;
  document.getElementById('name').placeholder = data.name;
  document.getElementById('email').placeholder = data.email;
  document.getElementById('subject').placeholder = data.subject;
  document.getElementById('message').placeholder = data.message;
  document.getElementById('submit').innerText = data.submit;
  document.getElementById('contact_us').innerHTML = data.contact_us;
  document.getElementById('address').innerHTML = data.address;
  document.getElementById('phone').innerHTML = data.phone;
  document.getElementById('email_contact').innerHTML = data.email_contact;
  document.getElementById('fhome').innerText = data.fhome;
  document.getElementById('fabout').innerText = data.fabout;
  document.getElementById('fcontact').innerText = data.fcontact;
  document.getElementById('fmore').innerText = data.fmore;
}

//loadContentContact();
