window.onselect = selectText;
let selection = "";
let currentLanguage = getBrowserLanguage() || "en";
let selectedWordsMap = new Map();

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

//test text to copy and paste: Ich gehe abends im Park joggen mit meinem Bruder nachdem wir gegessen haben und fühle mich glücklich dabei!
function selectText(e) {
  let textarea = document.getElementById("textfeld");
  let start = e.target.selectionStart;
  let end = e.target.selectionEnd;
  selection = getWholeTerm(textarea.value, start, end).word;
}

function submitClosedData() {
  fetch("/data", {
    method: "GET",
  }).then((response) => {
    console.log("Server response: ", response);
    window.location.href = "bedankung.html";
    return response.json();
  });
}

// Function to check if the textfield is empty
function checkTextfeld() {
  let textfeldWert = document.getElementById("textfeld").value.trim();

  if (textfeldWert === "") {
    handleEmptyFieldError();
    return false;
  } else {
    if (!hasBehaviorMarked()) {
      handleEmptyBehaviorError();
      return false;
    } else {
      submitClosedData();
      return true;
    }
  }
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

function hasBehaviorMarked() {
  for (const value of selectedWordsMap.values()) {
    if (value.button == "Behavior") {
      return true;
    }
  }
  return false;
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

function getWholeTerm(text, start, end) {
  // check if selection start is boundary of word
  let startBoundary = /\s/.test(text.charAt(start));
  while (start > 0 && !startBoundary) {
    start--;
    startBoundary = /\s/.test(text.charAt(start));
  }

  // check if selection end is boundary of word
  let endBoundary = /\s/.test(text.charAt(end));
  while (end < text.length && !endBoundary) {
    end++;
    endBoundary = /\s/.test(text.charAt(end));
  }

  if (start != 0) {
    start++;
  }

  return { word: text.substring(start, end).trim(), start: start, end: end };
}

function isHighlighted(highlightedWord, selectedMap) {
  // check if some of the new highlighted words are already highlighted
  let keysToDelete = [];
  for (const keys of selectedMap.keys()) {
    for (const entry of highlightedWord) {
      if (keys.includes(entry)) {
        keysToDelete.push(keys);
      }
    }
  }
  // return an array with only unique entries
  return [...new Set(keysToDelete)];
}

loadContentClosed();
