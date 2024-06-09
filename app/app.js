import express from 'express';
import sparqlClient from 'sparql-http-client';
import { v4 as uuid } from 'uuid';

import { translate } from 'deeplx';

import { config } from './utils/config.js';
import { staticFileMiddleware } from './middleware/staticFileMiddleware.js';
import { jsonBodyParser } from './middleware/requestParser.js';

import { initLanguage } from './controllers/languageController.js';

// Express config

import donateRouter from './routes/donateRouter.js';
import aboutRouter from './routes/aboutRouter.js';
import languageRouter from './routes/languageRouter.js';


const app = express();
const port = config.port;

// SPARQL client config
const db_user = config.db.user;
const db_pass = config.db.password;
const db_endpoint = config.getDbEndpoint();
const db_headers = config.getDbHeader();

// Middleware to parse form data in the request body
app.use(jsonBodyParser);

//Middleware to serve static files
app.use(staticFileMiddleware);

let selectionDataClosed = new Map();
let dataOpen;
let dataLanguage;
let inputSource;
let group_sql;

app.use((req, res, next) => {
  const lang = req.acceptsLanguages('de', 'en');
  //console.log(req.headers['accept-language']);
  //console.log('Accepted browser language:', lang);
  if (lang) {
    req.lang = lang;
  } else {
    req.lang = 'en';
  }
  initLanguage(lang);
  next();
})

// Routes
app.get('/', (req, res) => {
  res.redirect(301, '/donate');
});
app.use('/donate', donateRouter);
app.use('/about', aboutRouter);
app.use('/clang', languageRouter);
/*app.use(
  middleware.handle(i18next, {
    ignoreRoutes: ["/foo"], // or function(req, res, options, i18next)
    removeLngFromUrl: false
  })
)*/

/* eslint-disable */
//SPARQL Connection
async function insertDataClosed() {
  const keys = Array.from(selectionDataClosed.keys());
  console.log('Keys:', keys, keys.length);
  console.log('Inserting closed data into', db_endpoint);
  const habituuid = uuid.v4();
  const client = new sparqlClient({
    updateUrl: db_endpoint,
    user: db_user,
    password: db_pass,
    headers: db_headers,
  });

  let closedQuery = `
  PREFIX hhh: <http://example.com/hhh#>
  PREFIX owl: <http://www.w3.org/2002/07/owl#>
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX xml: <http://www.w3.org/XML/1998/namespace>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  BASE <http://www.w3.org/2002/07/owl#>

  INSERT DATA {
    hhh:ExperimentalSetting-${habituuid} rdf:type owl:NamedIndividual,
                                          hhh:${group_sql}.
                   
  `;

  //this adds the data according to user input to the query
  let i = 0;
  while (i < keys.length) {
    if (i == keys.length - 1) {
      closedQuery += `
      hhh:Behaviour-${habituuid} rdf:type owl:NamedIndividual,
                    hhh:${keys[i]} ; 
                              hhh:partOf hhh:ExperimentalSetting-${habituuid};
                              hhh:id "${habituuid}" ;
                              hhh:language "${dataLanguage}"^^rdf:langString;
                              hhh:source "${inputSource}"^^rdfs:Literal;
                              hhh:value "${await translate(
                                selectionDataClosed.get(keys[i]),
                                'en',
                                dataLanguage,
                              )}".
                              `;
      break;
    } else {
      closedQuery += `
        hhh:Behaviour-${habituuid} rdf:type owl:NamedIndividual,
                    hhh:${keys[i]} ; 
                              hhh:partOf hhh:ExperimentalSetting-${habituuid};
                              hhh:id "${habituuid}" ;
                              hhh:language "${dataLanguage}"^^rdf:langString;
                              hhh:source "${inputSource}"^^rdfs:Literal;
                              hhh:value "${await translate(
                                selectionDataClosed.get(keys[i]),
                                'en',
                                dataLanguage,
                              )}".
                              `;
    }
    i++;
  }

  closedQuery += `}`;
  try {
    await client.query.update(closedQuery);
    console.log('Data inserted successfully uuid:', habituuid);
  } catch (error) {
    console.debug(closedQuery);
    console.error('Error inserting data:', error.message);
  }
}

async function insertDataOpen() {
  console.log('Inserting open data into', db_endpoint);
  const habituuid = uuid.v4();
  const client = new sparqlClient({
    updateUrl: db_endpoint,
    user: db_user,
    password: db_pass,
    headers: db_headers,
  });
  let openQuery = `
  PREFIX hhh: <http://example.com/hhh#>
  PREFIX owl: <http://www.w3.org/2002/07/owl#>
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX xml: <http://www.w3.org/XML/1998/namespace>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  BASE <http://www.w3.org/2002/07/owl#>

  INSERT DATA {
    hhh:ExperimentalSetting-${habituuid} rdf:type owl:NamedIndividual,
                                          hhh:${group_sql}.

    hhh:Behaviour-${habituuid} rdf:type owl:NamedIndividual,
                hhh:Behaviour ; 
                          hhh:partOf hhh:ExperimentalSetting-${habituuid};
                          hhh:id "${habituuid}" ;
                          hhh:language "${dataLanguage}"^^rdf:langString;
                          hhh:source "${inputSource}"^^rdfs:Literal;
                          hhh:value "${await translate(
                            dataOpen,
                            'en',
                            dataLanguage,
                          )}".
    }`;

  try {
    await client.query.update(openQuery);
    console.log('Data inserted successfully uuid:', habituuid);
  } catch (error) {
    console.debug(openQuery);
    console.error('Error inserting data:', error.message);
  }
}

app.listen(port, () => {
  console.log(`Server is running on http://app.localhost`);
});
