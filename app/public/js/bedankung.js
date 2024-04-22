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
function navigateHomePage() {
    //clear map from the server (remove all data)
    fetch('/clearMap', {
    method: 'DELETE',
    })
    .then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    console.log('Map cleared successfully');
    })
    .catch(error => {
    console.error('Error:', error);
    });

    // Hier den vollständigen Pfad zur open.html-Datei angeben
    window.location.href = "http://app.localhost/donate"
}


// Function to change the language
function changeLanguage(lang) {
    currentLanguage = lang;
    loadContentBedankung();
}

// Function to load content based on the selected language
function loadContentBedankung() {
console.log('Loading content (Bedankung) for language:', currentLanguage);
    fetch('language/bedankung_language.json')
        .then(response => response.json())
        .then(data => {
            const navbarData = data[currentLanguage].navbar;
            const ContentData = data[currentLanguage].Contentbox;
            updateContent(navbarData);
            updateContentbox(ContentData);
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
function updateContentbox(data) {
    document.getElementById('slogan').innerHTML = data.slogan;
    document.getElementById('bedankung').innerHTML = data.bedankung;
    document.getElementById('donate_again').innerHTML = data.donate_again;
    document.getElementById('reward').innerHTML = data.reward;
    document.getElementById('fhome').innerText = data.fhome;
    document.getElementById('fabout').innerText = data.fabout;
    document.getElementById('fcontact').innerText = data.fcontact;
    document.getElementById('fmore').innerText = data.fmore;
}

loadContentBedankung();