// Load language JSON Files
import data_de from '../language/messages_de.json' with {type: 'json'};
import data_en from '../language/messages_en.json' with {type: 'json'};

let language = null;

export function getLanguageMessages() {
  if ( language.startsWith('de') ) {
    //console.log('AppLanguage is DE');
    return data_de;
  } else {
    //console.log('AppLanguage is EN');
    return data_en;
  }
}

export function initLanguage(lang) {
  if (language == null) {
    language = lang;
    console.log('Set app language to', language.toUpperCase());
  } /*else {
    console.log('App language is already set to', language);
  }*/
}

export function setLanguage(req, res) {
  console.log('Change app language to', req.body.language.toUpperCase());
  console.log(typeof(req.body.language));
  language = req.body.language;
  res.sendStatus(200);
}