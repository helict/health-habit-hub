import fs from 'fs';
import path, { dirname } from 'path';
import { fileURLToPath } from 'url';
import { hide_about } from './language_config.js';

let languageDataMap = new Map();

/**
 * Imports selected files dynamicly from the /language/ folder and collects them in a map.
 *
 * The function iterates over every file in the /language/ folder and imports all files whose filename matches a certain pattern.
 * These are then mapped to the corresponding language codes.
 */
export function loadLanguageFiles() {
  const __dirname = dirname(fileURLToPath(import.meta.url));

  let rawJson;
  let parsedJson;
  let languageFiles = fs.readdirSync(path.join(__dirname, '..', 'language'));

  languageFiles.forEach((file) => {
    if (path.basename(file).match(/messages_\w\w\.json/)) {
      rawJson = fs.readFileSync(path.join(__dirname, '..', 'language', file));
      parsedJson = JSON.parse(rawJson);
      languageDataMap.set(parsedJson.navigation.languageCode, parsedJson);

      //console.log('Languagefile loaded:', file, 'with Code:', parsedjson.navigation.languageCode)
    }
  });

  addAllLanguages();
  configureData();
}

/**
 * Extends the JSON files with a map consisting of all languages and language codes.
 *
 * The function iterates over all language files and builds a new map that maps all languages in the national language to the corresponding language codes.
 * The new map is then added to each language file.
 */
function addAllLanguages() {
  let allLanguages = new Map();

  languageDataMap.values().forEach((data) => {
    allLanguages.set(data.navigation.language, data.navigation.languageCode);
  });

  languageDataMap.values().forEach((data) => {
    data.navigation.allLanguages = allLanguages;
  });

  //console.log(allLanguages);
}

function configureData() {
  languageDataMap.values().forEach((data) => {
    //console.log(data.navigation.languageCode, ':', hide_about.includes(data.navigation.languageCode))
    if (hide_about.includes(data.navigation.languageCode)) {
      data.navigation.show_about = 1;
    } else {
      data.navigation.show_about = 0;
    }
  });
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
