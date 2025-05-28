import SparqlClient from 'sparql-http-client';
// import { translate } from 'deeplx';
import fetch from 'node-fetch'; // to make HTTP POST request to LibreTranslate API
import { v4 as uuidv4 } from 'uuid';
import { config } from './config.js';

// function to translate text using LibreTranslate API
async function libreTranslate(text, from, to) {
  try {
    const response = await fetch(config.getTranslationApiEndpoint(), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        q: text,
        source: from,
        target: to,
        format: 'text',
      }),
    })
      .then(console.debug)
      .catch(console.error);

    if (!response.ok) {
      throw new Error(`Translation failed: ${response.statusText}`);
    }

    const data = await response.json();
    return data.translatedText;
  } catch (err) {
    console.error('LibreTranslate error:', err);
    throw err;
  }
}

class DbClient {
  constructor(config) {
    this.client = new SparqlClient({
      updateUrl: config.getDbEndpoint(),
      user: config.db.user,
      password: config.db.password,
      headers: config.getDbHeader(),
    });
  }

  async insertData(query) {
    try {
      await this.client.query.update(query);
      console.log('Data inserted successfully');
    } catch (error) {
      console.debug(query);
      console.error('Error inserting data:', error.message);
    }
  }

  async insertDonateData(data) {
    console.log('Inserting donation data:', data);
    const experimentGroup = data.experimentGroup;
    const habituuid = uuidv4();
    const source =
      data.language.toLowerCase() === 'en' ? 'user' : 'libretranslate';
    const value =
      source === 'user'
        ? data.inputValue
        : await libreTranslate(data.inputValue, data.language, 'en');

    let query = `
    PREFIX hhh: <http://example.com/hhh#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xml: <http://www.w3.org/XML/1998/namespace>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    BASE <http://www.w3.org/2002/07/owl#>
    
    INSERT DATA {
      hhh:ExperimentalSetting-${habituuid} rdf:type owl:NamedIndividual,
                                            hhh:${experimentGroup.toString()}.
    `;

    if (experimentGroup.closedTask) {
      for (const context of data.contexts) {
        query += `
      hhh:Behaviour-${habituuid} rdf:type owl:NamedIndividual,
                  hhh:${context.name} ;
                            hhh:partOf hhh:ExperimentalSetting-${habituuid};
                            hhh:id "${habituuid}" ;
                            hhh:language "${data.language}"^^rdf:langString;
                            hhh:source "${source}"^^rdfs:Literal;
                            hhh:value "${await libreTranslate(
                              context.value,
                              data.language,
                              'en'
                            )}".
      `;
      }
    } else {
      query += `
      hhh:Behaviour-${habituuid} rdf:type owl:NamedIndividual,
                  hhh:Behaviour ;
                            hhh:partOf hhh:ExperimentalSetting-${habituuid};
                            hhh:id "${habituuid}" ;
                            hhh:language "${data.language}"^^rdf:langString;
                            hhh:source "${source}"^^rdfs:Literal;
                            hhh:value "${await value}".
    `;
    }

    query += `}`;

    await this.insertData(query);
  }
}

export { DbClient };
