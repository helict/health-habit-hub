import { createRequire } from "module";
const require = createRequire(import.meta.url);

import { translate } from "deeplx";
import { dirname } from "path";
import { fileURLToPath } from "url";

const express = require("express");
const sparqlClient = require("sparql-http-client");
const uuid = require("uuid");
const path = require("path");

const requestMiddlewares = require("./middleware/requestParser.cjs");
const staticFileMiddleware = require("./middleware/staticFileMiddleware.cjs");

import donateRouter from "./routers/donateRouter.js";

import aboutRouter from './routes/aboutRouter.js';

// Express config
const app = express();
const port = 3000;

// SPARQL client config
const db_user = "admin";
const db_pass = "admin";
const db_proto = "http";
const db_host = "fuseki";
const db_port = "3030";
const db_name = "hhh";
const db_endpoint = db_proto + "://" + db_host + ":" + db_port + "/" + db_name;
const db_headers = [
  ["host", db_host],
  ["port", db_port],
  ["path", "/" + db_name],
];

const __dirname = dirname(fileURLToPath(import.meta.url));

// Middleware to parse form data in the request body
app.use(requestMiddlewares.jsonBodyParser);

//Middleware to serve static files
app.use(staticFileMiddleware.staticFileMiddleware);

let selectionDataClosed = new Map();
let dataOpen;
let dataLanguage;
let inputSource;
let group_sql;

// Routes
app.get("/", (req, res) => {
  res.redirect(301, "/donate");
});
app.use("/donate", donateRouter);

//SPARQL Connection
async function insertDataClosed() {
  const keys = Array.from(selectionDataClosed.keys());
  console.log("Keys:", keys, keys.length);
  console.log("Inserting closed data into", db_endpoint);
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
                                "en",
                                dataLanguage
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
                                "en",
                                dataLanguage
                              )}".
                              `;
    }
    i++;
  }

  closedQuery += `}`;
  try {
    await client.query.update(closedQuery);
    console.log("Data inserted successfully uuid:", habituuid);
  } catch (error) {
    console.debug(closedQuery);
    console.error("Error inserting data:", error.message);
  }
}

async function insertDataOpen() {
  console.log("Inserting open data into", db_endpoint);
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
                            "en",
                            dataLanguage
                          )}".
    }`;

  try {
    await client.query.update(openQuery);
    console.log("Data inserted successfully uuid:", habituuid);
  } catch (error) {
    console.debug(openQuery);
    console.error("Error inserting data:", error.message);
  }
}

app.listen(port, () => {
  console.log(`Server is running on http://app.localhost`);
});
