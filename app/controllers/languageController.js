// Load language JSON Files
import data_de from '../language/messages_de.json' with {type: 'json'};
import data_en from '../language/messages_en.json' with {type: 'json'};

let language = null;

export function getLanguageMessages() {
  let usedLang = getLanguage();
  
  if ( usedLang.startsWith('de') ) {
    console.log('Used Language is DE');
    return data_de;
  } else {
     console.log('Used Language is EN');
    return data_en;
  }
  }

  function getLanguage() {
    console.log(language);
    if (language == null) {
      // Versuche, die bevorzugte Sprache des Browsers zu erhalten
      language = (navigator.language || navigator.userLanguage);
      console.log(navigator.languages);
    }
    return language;
  }
  
  //just play - not USED
  function isLanguageAccepted(request, response) {
    var lang = request.acceptsLanguages('de', 'en');
    if (lang) {
        console.log('The first accepted of [fr, es, en] is: ' + lang);
    } else {
        console.log('None of [de, en] is accepted');
    }
  }
  
  export function setLanguage(req, res) {
    console.log('Received language data:', req.body);
    let data = req.body;
    language = data.language;
    res.sendStatus(200);
  }