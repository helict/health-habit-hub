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
    loadContentOpenhybrid();
}

//receive form data from opem.html
function sendOpenHybridData(){
    let openData = document.getElementById('textfeld').value;
    console.log('Saving selection:', openData, typeof openData);
    fetch('/save-selection-open-hybrid', {
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

function submitOpenHybridData(){
  sendOpenHybridData();  
  fetch('/data', {
      method: 'GET',
    })
    .then(response => {
      console.log("Server response: ", response);
      window.location.href = 'bedankung.html';
      return response.json()})
  }

function checkTextfeld() {
    let textfeldWert = document.getElementById("textfeld").value.trim();

    if (textfeldWert === "") {
        handleEmptyFieldError();
        return false;
    } else {
        submitOpenHybridData();
        return true;
    }
}

function handleEmptyFieldError() {
    fetch('language/openhybrid_language-data.json')
        .then(response => response.json())
        .then(data => {
            const fehlerText = data[currentLanguage].emptyFieldError;
            alert(fehlerText);
        })
        .catch(error => console.error('Error loading language data file:', error));
}

// Function to load content based on the selected language
function loadContentOpenhybrid() {
    console.log('Loading content (openhybrid) for language:', currentLanguage);
    fetch('language/openhybrid_language-data.json')
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
    document.getElementById('header').innerText = data.header;
    document.getElementById('intro-text').innerHTML = data.text;        
    document.getElementById('step2').innerHTML = data.step2;
    document.getElementById('submit').innerHTML = data.submit;
    document.getElementById('fhome').innerText = data.fhome;
    document.getElementById('fabout').innerText = data.fabout;
    document.getElementById('fcontact').innerText = data.fcontact;
    document.getElementById('fmore').innerText = data.fmore;
  

  
}

loadContentOpenhybrid();

