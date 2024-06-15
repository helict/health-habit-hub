// Load language JSON Files
import data_de from '../language/messages_de.json' with { type: 'json' };
import data_en from '../language/messages_en.json' with { type: 'json' };
import data_ja from '../language/messages_ja.json' with { type: 'json' };

let language = null;

/**
 * Determines the language to be used based on the user's language preference and returns the corresponding language data.
 *
 * This function checks if the language starts with 'de' and returns the corresponding language data ('data_de' or 'data_en').
 *
 * @returns {object} - Returns the corresponding language data to the selected/preferred language.
 */
export function getLanguageMessages() {
  if (language.startsWith('de')) {
    //console.log('AppLanguage is DE');
    return data_de;
  } else if (language.startsWith('ja')) {
    return data_ja;
  } else {
    //console.log('AppLanguage is EN');
    return data_en;
  }
}

/**
 * Initializes the application's language based on the preferred brwoser language.
 *
 * This function checks whether the global variable language is already set. If not, the variable is overwritten with the value of the transferred parameter and logged.
 *
 * @param {object} lang - The object, which contains the preferred browser language.
 */
export function initLanguage(lang) {
  if (language == null) {
    language = lang;
    console.log('Set app language to', language.toUpperCase());
  } /*else {
      console.log('App language is already set to', language);
    }*/
}

/**
 * Sets the application's language based on the incoming request data and sends a response status.
 *
 * This function logs the received language property from the request body, extracts and assigns it to a global variable 'language'.
 * After that it sends a 200 OK status response.
 *
 * @param {object} req - The request object, which contains the HTTP request data. The language information is expected to be in the body of this request.
 * @param {object} res - The response object, used to send a response back to the client.
 */
export function setLanguage(req, res) {
  console.log('Change app language to', req.body.language.toUpperCase());
  language = req.body.language;
  res.sendStatus(200);
}
