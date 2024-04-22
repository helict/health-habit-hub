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
    loadContentAbout();
}

// Function to load content based on the selected language
function loadContentAbout() {
    console.log('Loading content (about) for language:', currentLanguage);
    fetch('language/about_language-data.json')
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
    document.getElementById('about_text').innerHTML = data.about_text;
    document.getElementById('step3').innerHTML = data.step3;
    document.getElementById('fhome').innerText = data.fhome;
    document.getElementById('fabout').innerText = data.fabout;
    document.getElementById('fcontact').innerText = data.fcontact;
    document.getElementById('fmore').innerText = data.fmore;
}

loadContentAbout();

