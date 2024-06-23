// Load language JSON Files
import data_de from '../language/messages_de.json' with { type: 'json' };
import data_en from '../language/messages_en.json' with { type: 'json' };
import data_ja from '../language/messages_ja.json' with { type: 'json' };

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
  switch(lang) {
    case 'de':
      //console.log('AppLanguage is DE');
      return data_de;
    case 'ja':
      //console.log('AppLanguage is JA');
      return data_ja;
    default:
      //console.log('AppLanguage is EN');
      return data_en;
  }
}
