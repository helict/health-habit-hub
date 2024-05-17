let currentLanguage = getBrowserLanguage() || "en";

function getBrowserLanguage() {
  // Versuche, die bevorzugte Sprache des Browsers zu erhalten
  let browserLanguage = navigator.language || navigator.userLanguage;

  if (
    browserLanguage &&
    (browserLanguage === "de" || browserLanguage.startsWith("de-"))
  ) {
    return "de";
  } else {
    return "en";
  }
}
// Function to change the language
function changeLanguage(lang) {
  currentLanguage = lang;
  loadContentClosed();
}

function handleEmptyFieldError() {
  fetch("language/language-data.json")
    .then((response) => response.json())
    .then((data) => {
      const fehlerText = data[currentLanguage].emptyFieldError;
      alert(fehlerText);
    })
    .catch((error) =>
      console.error("Error loading language data file:", error)
    );
}

function handleEmptyBehaviorError() {
  fetch("language/language-data.json")
    .then((response) => response.json())
    .then((data) => {
      const fehlerText = data[currentLanguage].emptyBehaviorError;
      alert(fehlerText);
    })
    .catch((error) =>
      console.error("Error loading language data file:", error)
    );
}

function loadContentClosed() {
  console.log("Loading content (closed) for language:", currentLanguage);
  fetch("language/language-data.json")
    .then((response) => response.json())
    .then((data) => {
      const { navbar, introduction, datadonation, Greybox } =
        data[currentLanguage];

      updateContent(navbar);
      updateIntroduction(introduction);
      updateDatadonation(datadonation);
      updateGreybox(Greybox);
    })
    .catch((error) =>
      console.error("Error loading language data file:", error)
    );
}

// Function to update the Introduction content on the page
function updateContent(data) {
  document.getElementById("nav-home").innerText = data.home;
  document.getElementById("nav-about").innerText = data.about;
  document.getElementById("nav-contact").innerText = data.contact;
}

// Function to update the Introduction content on the page
function updateIntroduction(data) {
  document.getElementById("header").innerHTML = data.header;
  document.getElementById("intro-text").innerHTML = data.text;
}

// Function to update the green datadonation content on the page
function updateDatadonation(data) {
  document.getElementById("step2").innerHTML = data.step2;
}

// Function to update the greybox content on the page
function updateGreybox(data) {
  document.getElementById("example1").innerHTML = data.example1;
  document.getElementById("clear").innerHTML = data.clear;
  document.getElementById("time").innerText = data.time;
  document.getElementById("physical").innerText = data.physical;
  document.getElementById("prior").innerText = data.prior;
  document.getElementById("people").innerText = data.people;
  document.getElementById("internal").innerText = data.internal;
  document.getElementById("behavior").innerText = data.behavior;

  document.getElementById("step3").innerHTML = data.step3;
  //document.getElementById('example2').innerHTML = data.example2;
  document.getElementById("submit").innerHTML = data.submit;
  document.getElementById("fhome").innerText = data.fhome;
  document.getElementById("fabout").innerText = data.fabout;
  document.getElementById("fcontact").innerText = data.fcontact;
  document.getElementById("fmore").innerText = data.fmore;
  document.getElementById("add").innerText = data.add;
}

loadContentClosed();
