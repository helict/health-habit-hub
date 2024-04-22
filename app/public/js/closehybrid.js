window.onselect = selectText;
let selection = '';
let currentLanguage = getBrowserLanguage() || 'en';
let selectedWordsMap = new Map();
let wordIdMap = new Map();


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
    loadContentClosehybrid();
}

//test text to copy and paste: Ich gehe abends im Park joggen mit meinem Bruder nachdem wir gegessen haben und fühle mich glücklich dabei!
function selectText(e)
{
    let textarea = document.getElementById("textfeld");
    let start = e.target.selectionStart;
    let end = e.target.selectionEnd;
    selection = getWholeTerm(textarea.value, start, end).word;
}


function saveSelection(button_name)
{
    let sel_data =selection;
    highlightWords(button_name)
    console.log('Saving selection:', sel_data, typeof sel_data);
    fetch('/save-selection-closed-hybrid', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(
          {button_name, sel_data, language: currentLanguage})
    })
    .then(response => {
      console.log("Server response: ", response);
      return response.json()
    })
    .then(sel_data => console.log(sel_data))
    .catch(err => console.error(err));
    selection = '';
}

function submitClosedHybridData(){
    fetch('/data', {
      method: 'GET',
    })
    .then(response => {
      console.log("Server response: ", response);
      window.location.href = 'bedankung.html';
      return response.json()})
}

// Function to check if the textfield is empty
function checkTextfeld() {
  let textfeldWert = document.getElementById("textfeld").value.trim();

  if (textfeldWert === "") {
      handleEmptyFieldError();
      return false;
  } else {
    if (!hasBehaviorMarked()) {
      handleEmptyBehaviorError()
      return false;
    }
    else {
      submitClosedHybridData();
      return true;
    }
  }
}

function handleEmptyFieldError() {
  fetch('language/language-data.json')
      .then(response => response.json())
      .then(data => {
          const fehlerText = data[currentLanguage].emptyFieldError;
          alert(fehlerText);
      })
      .catch(error => console.error('Error loading language data file:', error));
}

function handleEmptyBehaviorError() {
  fetch('language/language-data.json')
    .then(response => response.json())
    .then(data => {
        const fehlerText = data[currentLanguage].emptyBehaviorError;
        alert(fehlerText);
    })
    .catch(error => console.error('Error loading language data file:', error));
}

function hasBehaviorMarked() {
  for (const value of selectedWordsMap.values()) {
    if (value.button == "Behavior") {
      return true;
    }
  }
  return false;
}


function loadContentClosehybrid() {
    console.log('Loading content (closehybrid) for language:', currentLanguage);
    fetch('language/language-data.json')
        .then(response => response.json())
        .then(data => {
            const { navbar, datadonation, Greybox } = data[currentLanguage];
            updateContent(navbar);
            updateDatadonation(datadonation);
            updateGreybox(Greybox);
        })
        .catch(error => console.error('Error loading language data file:', error));
}

// Function to update the Introduction content on the page
function updateContent(data) {
    document.getElementById('nav-home').innerText = data.home;
    document.getElementById('nav-about').innerText = data.about;
    document.getElementById('nav-contact').innerText = data.contact;
}


// Function to update the green datadonation content on the page
function updateDatadonation(data) {
    document.getElementById('step2').innerHTML = data.step2;
}
// Function to update the greybox content on the page
function updateGreybox(data) {
    document.getElementById('example1').innerHTML = data.example1;
    document.getElementById('clear').innerHTML = data.clear;
    document.getElementById('time').innerText = data.time;
    document.getElementById('physical').innerText = data.physical;
    document.getElementById('prior').innerText = data.prior;
    document.getElementById('people').innerText = data.people;
    document.getElementById('internal').innerText = data.internal;
    document.getElementById('behavior').innerText = data.behavior;

    document.getElementById('step3').innerHTML = data.step3;
    //document.getElementById('example2').innerHTML = data.example2;
    document.getElementById('submit').innerHTML = data.submit;
    document.getElementById('fhome').innerText = data.fhome;
    document.getElementById('fabout').innerText = data.fabout;
    document.getElementById('fcontact').innerText = data.fcontact;
    document.getElementById('fmore').innerText = data.fmore;
    document.getElementById('add').innerText = data.add;
    document.getElementById('behavior').innerText = data.behavior; 
}

function onInput() {
    copyText();
    setID(); 
    trackChanges();
  }
  
  function copyText()
  {
    // copy value of textarea and insert it to textbox
    let textareaValue = document.getElementById("textfeld").value;
    document.getElementById("example2").innerText = textareaValue;
  
     // reapply highlighting for existing highlighted words
     document.getElementById("example2").innerHTML = applyHighlights(textareaValue);
  }
  
  function setID() {
    let textarea = document.getElementById('textfeld');
    let textareaValue = textarea.value;
  
    let words = textareaValue.split(' ');
    
    let button = null;
    // clear previous entries in the Map
    wordIdMap.clear();
  
    // create a map to store arrays of objects for each word
    let wordOccurrenceMap = new Map();
  
    // add IDs, start, and end positions to each word and store in the Map
    for (let i = 0, pos = 0; i < words.length; i++) {
      let word = words[i];
  
      // get or create an array for the current word in the map
      let wordOccurrences = wordOccurrenceMap.get(word) || [];
      
      // create a unique ID 
      let wordId = 'word-' + i;
  
      let start = pos;
      let end = pos + word.length;
  
      wordOccurrences.push({ id: wordId, start, end });
  
      // update the array in the map
      wordOccurrenceMap.set(word, wordOccurrences);
  
      // update the position for the next word (considering space)
      pos += word.length + 1;
    }
  
    wordOccurrenceMap.forEach((occurrences, word) => {
      occurrences.forEach(({ id, start, end }) => {
        wordIdMap.set(id, { word, start, end, button});
      });
    });
  
    console.log(wordIdMap);
  }
  
  function trackChanges() {
    
    let textarea = document.getElementById('textfeld');
  
    let previousContent = textarea.value;
  
    textarea.addEventListener('input', function(event) {
      let currentContent = event.target.value;
      // comparing previous and current content
      let result = findChangedWord(previousContent, currentContent);
      console.log(result);
  
      // remove highlighting if word was changed
      selectedWordsMap.forEach(function(value, id){
        let words = value.word.split(/\W+/);
  
        if (words.indexOf(result.previousState) !== -1) {
          removeHighlight(id)
          console.log("Done")
        }
      })
  
      // update the previousContent for next comparison
      previousContent = currentContent;
    });
  }
  
  function findChangedWord(previousContent, currentContent) {
    // create array for previous words and current words
    let previousWords = previousContent.split(/\s+/);
    let currentWords = currentContent.split(/\s+/);
  
    for (let i = 0; i < currentWords.length; i++) {
      if (previousWords[i] != currentWords[i]) {
        return {
          previousState: previousWords[i],
          changedWord: currentWords[i]
        }
      }
    }
  }
  
  function applyHighlights(highlightedText) {
  
    const replacements = [];
  
    // apply highlighting for each word in array
    selectedWordsMap.forEach(function (value, id) {
  
      const { word, start, end } = value;
  
      // apply highlighting for the specified word
      const escapedWord = word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const regex = new RegExp('(\\b|\\s|^)' + escapedWord + '(\\b|\\s|$)', 'gi');
      const replacement = `<span class="highlighted-${value.button}">$&</span>`;
  
      // adding information to array, because positions are changing after applying highlights because of inserting html code
      replacements.push({
        start: start,
        end: end,
        replacement: replacement,
        regex: regex,
      });
    });
  
    // sort replacements by start position in descending order
    replacements.sort((a, b) => b.start - a.start);
    
    // apply replacements to the highlightedText
    replacements.forEach((replacement) => {
      let beforeHighlighted = highlightedText.slice(0, replacement.start);
      let highlightedWord = highlightedText.slice(replacement.start, replacement.end).replace(replacement.regex, replacement.replacement);
      let afterHighlighted = highlightedText.slice(replacement.end);
  
      highlightedText = beforeHighlighted + highlightedWord + afterHighlighted
  
    });
  
    console.log('Highlighted Text:', highlightedText);
  
    return highlightedText;
  }
  
  function getWholeTerm(text, start, end) {
    // check if selection start is boundary of word
    let startBoundary = /\s/.test(text.charAt(start));
    while(start > 0 && !startBoundary) {
        start--;
        startBoundary = /\s/.test(text.charAt(start));
    }
  
    // check if selection end is boundary of word
    let endBoundary = /\s/.test(text.charAt(end));
    while(end < text.length && !endBoundary) {
        end++;
        endBoundary = /\s/.test(text.charAt(end));
    }
  
    if (start != 0) {
      start++;
    }
  
    return { word: text.substring(start, end).trim(), start: start, end: end };
  }
  
  function removeHighlight(id) {
    let content = document.getElementById('example2');
  
    let keyArr = isHighlighted(id, selectedWordsMap)
    
    keyArr.forEach(key => {
      button = selectedWordsMap.get(key).button
      // replace the highlighted span with the original word
      content.innerHTML = content.innerHTML.replace(
      new RegExp(`<span class="highlighted-${key}">\\b${selectedWordsMap.get(key).word}\\b</span>`, 'gi'),
      selectedWordsMap.get(key).word
      );
  
      // remove the word from the selectedWordsMap
      selectedWordsMap.delete(key);
      // remove word from the server 
      fetch('/deleteWord', {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ button: button }),
        })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        console.log(`Word successfully removed from map`);
      })
      .catch(error => {
        console.error('Error:', error);
      });
    });
  }
  
  function removeAllHighlights() {
    //remove all highlighting and reset the selectedWordsMap and the textbox
    let textareaValue = document.getElementById("textfeld").value;
    let content = document.getElementById('example2');
  
    selectedWordsMap.clear()
    content.innerText = textareaValue;
  
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
  }
  
  function getWordIdByPosition(start, end) {
    // tterate through the entries in wordIdMap
    for (const [id, { start: mapStart, end: mapEnd }] of wordIdMap.entries()) {
      if (mapStart === start && mapEnd === end) {
        // ff the start and end positions match, return the corresponding ID
        return id;
      }
    }
    // return null if no matching start and end positions are found in the map
    return null;
  }
  
  
  function getAllIDsBySelectedWord() {
  
    let textarea = document.getElementById('textfeld');
    let selectionStart = textarea.selectionStart;
    let selectionEnd = textarea.selectionEnd;
  
    let selectedText = getWholeTerm(textarea.value, selectionStart, selectionEnd);
  
    return {wordIds: separateWords(selectedText), words: selectedText.word, start: selectedText.start, end: selectedText.end}
  }
  
  function separateWords(data) {
  
    const words = data.word.split(' ');
    const ids = [];
  
    let currentStart = data.start;
  
    for (const word of words) {
      const currentEnd = currentStart + word.length;
      const wordId = getWordIdByPosition(currentStart, currentEnd);
  
      ids.push(wordId);
  
      // update the start position for the next word (considering space)
      currentStart = currentEnd + 1;
    }
    return ids;
  }
  
  function highlightWords(button) {
  
    let textarea = document.getElementById("textfeld");
    let wordsInfo = getAllIDsBySelectedWord();
  
    if (isHighlighted(wordsInfo.wordIds, selectedWordsMap).length > 0) {
      // remove old highlighting if there is an overlapping of highlighting
        removeHighlight(wordsInfo.wordIds);
        selectedWordsMap.set(wordsInfo.wordIds, {word: wordsInfo.words, start: wordsInfo.start, end: wordsInfo.end, button: button});
    } else {
      selectedWordsMap.set(wordsInfo.wordIds, {word: wordsInfo.words, start: wordsInfo.start, end: wordsInfo.end, button: button});
    }
  
    let content = document.getElementById('example2');
    content.innerHTML = applyHighlights(textarea.value);
  
  }
  
  function isHighlighted(highlightedWord, selectedMap) {
    // check if some of the new highlighted words are already highlighted
    let keysToDelete = []
    for (const keys of selectedMap.keys()) {
      for (const entry of highlightedWord) {
        if (keys.includes(entry)) {
          keysToDelete.push(keys)
        }
      }
    }
    // return an array with only unique entries 
    return [...new Set(keysToDelete)]
  }
  
  
loadContentClosehybrid();

