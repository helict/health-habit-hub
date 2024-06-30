// Load language JSON Files
// import data_de from '../language/messages_de.json' with { type: 'json' };
// import data_en from '../language/messages_en.json' with { type: 'json' };
// import data_ja from '../language/messages_ja.json' with { type: 'json' };

import fs from 'fs';

import path, { dirname } from 'path';
import { fileURLToPath } from 'url';


let languageDataMap = new Map()






export function loadLanguageFiles() {

  const __dirname = dirname(fileURLToPath(import.meta.url));

  let rawJson;
  let parsedJson;
  let languageFiles = fs.readdirSync(path.join(__dirname, '..', 'language'));

  languageFiles.forEach( file => {
    if (path.extname(file) == '.json')  // ggf. noch Dateinamen prüfen (messages_xx.json)
    {
        rawJson = fs.readFileSync(path.join(__dirname, '..', 'language',file));
        parsedJson = JSON.parse( rawJson );
        languageDataMap.set(parsedJson.navigation.languageCode, parsedJson);

        //console.log('Languagefile loaded:', file, 'with Code:', parsedjson.navigation.languageCode)
    }
  })

  addAllLanguages();
}

function addAllLanguages() {
  let allLanguages = new Map();

  languageDataMap.values().forEach(data => {
    allLanguages.set(data.navigation.language, data.navigation.languageCode);
  });

  languageDataMap.values().forEach(data => {
    data.navigation.allLanguages = allLanguages;
  });

  //console.log(allLanguages);
}

/**
 * Determines the language to be used based on the user's language preference and returns the corresponding language data.
 *
 * This function checks if the language starts with 'de' or 'ja' and returns the corresponding language data ('data_de' or 'data_en' or 'data_ja').
 * 
 * @param {object} lang - The object, which contains the preferred language.
 *
 * @returns {object} - Returns the corresponding language data to the selected/preferred language.
 */
export function getLanguageMessages(lang) {

  if (languageDataMap.has(lang)) {
    return languageDataMap.get(lang);
  }
  
  return languageDataMap.get('en');
}

export function getLanguageCodes() {
  //console.log(languageDataMap.keys());

  return Array.from(languageDataMap.keys());
}
