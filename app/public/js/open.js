let currentLanguage = getBrowserLanguage() || 'en';

function getBrowserLanguage() {
    // Versuche, die bevorzugte Sprache des Browsers zu erhalten
    let browserLanguage = navigator.language || navigator.userLanguage;

    if (browserLanguage && (browserLanguage === 'de' || browserLanguage.startsWith('de-'))) {
        return 'de';
    } else {
        return 'en';
    }
}

// Function to change the language
function changeLanguage(lang) {
    currentLanguage = lang;
    loadContentOpen();
}

//receive form data from opem.html
function sendOpenData(){
    let openData = document.getElementById('textfeld').value;
    console.log('Saving selection:', openData);
    fetch('/save-selection-open', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({data: openData, language: currentLanguage})
    })
    .then(response => {
      console.log("Server response: ", response);
      return response.json()
    })
    .then(sel_data => console.log(sel_data))
    .catch(err => console.error(err)); 
}

function submitOpenData(){
  sendOpenData();  
  fetch('/data', {
      method: 'GET',
    })
    .then(response => {
      console.log("Server response: ", response);
      window.location.href = 'bedankung.html';
      return response.json()})
  }

//generate random number on first site load with session storage
let rdmIntForSiteLoad
if (!sessionStorage.getItem('rdmIntForSiteLoad')) {
  rdmIntForSiteLoad = Math.floor(Math.random() * 1000);
  sessionStorage.setItem('rdmIntForSiteLoad', rdmIntForSiteLoad);
  console.log('Session Stroage no number: ', rdmIntForSiteLoad);
  callMainPage();
}else{
  rdmIntForSiteLoad = sessionStorage.getItem('rdmIntForSiteLoad');
  console.log('Session storage had number: ', rdmIntForSiteLoad);
  callMainPage();
}

function callMainPage(){
  fetch('/donate', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({rdmIntForSiteLoad})
})
  .then(response => {
    console.log("Server response: ", response);
    return response.json()
  })
  .then(serverResponse => console.log(serverResponse))
  .catch(err => console.error(err));
}


function checkTextfeld() {
    let textfeldWert = document.getElementById("textfeld").value.trim();

    if (textfeldWert === "") {
        handleEmptyFieldError();
        return false;
    } else {
        submitOpenData();
        return true;
    }
}

function handleEmptyFieldError() {
    fetch('language/open_language-data.json')
        .then(response => response.json())
        .then(data => {
            const fehlerText = data[currentLanguage].emptyFieldError;
            alert(fehlerText);
        })
        .catch(error => console.error('Error loading language data file:', error));
}

// Function to load content based on the selected language
function loadContentOpen() {
    console.log('Loading content (open) for language:', currentLanguage);
    fetch('language/open_language-data.json')
        .then(response => response.json())
        .then(data => {
            const navbarData = data[currentLanguage].navbar;
            const GreyboxData = data[currentLanguage].Greybox;
            updateContent(navbarData);
            updateGreybox(GreyboxData);
        })
        .catch(error => console.error('Error loading language data file:', error));
}

// Function to update the Introduction content on the page
function updateContent(data) {
    document.getElementById('nav-home').innerText = data.home;
    document.getElementById('nav-about').innerText = data.about;
    document.getElementById('nav-contact').innerText = data.contact;
}

// Function to update the greybox content on the page
function updateGreybox(data) {
    document.getElementById('step2').innerHTML = data.step2;
    document.getElementById('submit').innerHTML = data.submit;
    document.getElementById('fhome').innerText = data.fhome;
    document.getElementById('fabout').innerText = data.fabout;
    document.getElementById('fcontact').innerText = data.fcontact;
    document.getElementById('fmore').innerText = data.fmore;
}

loadContentOpen();

