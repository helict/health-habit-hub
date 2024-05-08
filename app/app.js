const createRequire = require('module').createRequire;

try {
  require('dotenv').config();
} catch (error) {
  console.error("Failed to load .env file", error);
}

const translate = require('deeplx').translate;
const dirname = require('path').dirname;
const fileURLToPath = require('url').fileURLToPath


const express = require('express');
const sparqlClient = require('sparql-http-client');
const uuid = require('uuid');
const path = require('path');

const requestMiddlewares = require('./middleware/requestParser.cjs');
const staticFileMiddleware = require('./middleware/staticFileMiddleware.cjs');

// Express config
const config = require('./EnvManager.js');

const app = express();
const port = config.port;

// SPARQL client config
const db_user = config.db.user
const db_pass = config.db.password
const db_proto = config.db.protocol
const db_host = config.db.host
const db_port = config.db.dbPort
const db_name = config.db.name
const db_endpoint = config.getDbEndpoint()
const db_headers = config.getDbHeader()


// Middleware to parse form data in the request body
app.use(requestMiddlewares.jsonBodyParser);

//Middleware to serve static files 
app.use(staticFileMiddleware.staticFileMiddleware);

let selectionDataClosed = new Map();
let dataOpen;
let methodData;
let dataLanguage;
let rdmInt;
let inputSource;
let group_sql;

// Routes
app.get('/donate', (req, res) => {
  console.log('Random Number used(get): ', rdmInt);
  if (rdmInt % 4 == 0) {
    res.sendFile(path.join(__dirname, 'public', 'closed.html'));
    console.log('Sending closed.html', rdmInt%4);
  } else if (rdmInt % 4 == 1) {
    res.sendFile(path.join(__dirname, 'public', 'closehybrid.html'));
    console.log('Sending closehybrid.html', rdmInt%4);
  } else if (rdmInt % 4 == 2) {
    res.sendFile(path.join(__dirname, 'public', 'open.html'));
    console.log('Sending open.html', rdmInt%4);
  } else {
    res.sendFile(path.join(__dirname, 'public', 'openhybrid.html'));
    console.log('Sending openhybrid.html', rdmInt%4);
  }
});

app.post('/donate', (req, res) => {
  if (req.body.rdmIntForSiteLoad != undefined) {
    if(req.body.rdmIntForSiteLoad == rdmInt) console.log('Same number used(post): ', rdmInt);
    console.log('Random Number used(post): ', req.body.rdmIntForSiteLoad, "before: ", rdmInt);
    rdmInt = req.body.rdmIntForSiteLoad;
    console.log('Random Number used(post): ', rdmInt);
    res.send('Number saved!');
  }else{
    console.log('Didnt get new number, used(post): ', rdmInt);
    res.send('Number not recieved, was undefined!');
  }
});


app.get('/closed', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'closed.html'));
  console.log('Sending closed.html via /closed');
});

app.get('/open', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'open.html'));
  console.log('Sending open.html via /open');
});

app.get("/openhybrid", (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'openhybrid.html'));
});

app.get("/closedhybrid", (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'closehybrid.html'));
});

app.post('/save-selection-closed', (req, res) => {
  console.log("got data - save-selection-closed:", req.body);
  selectionDataClosed.set(req.body.button_name, req.body.sel_data);
  methodData = "Closed Ended Data Entry"
  dataLanguage = req.body.language;
  console.log('Received Selection:', selectionDataClosed, 'Current Language: ', dataLanguage, "Method used: ", methodData); //for debugging
  res.send('Selection saved!');
});

app.post('/save-selection-closed-hybrid', (req, res) => {
  console.log("got data - save-selection-closed-hybrid:", req.body);
  selectionDataClosed.set(req.body.button_name, req.body.sel_data);
  methodData = "Closed Ended Hybrid Data Entry"
  dataLanguage = req.body.language;
  console.log('Received Selection:', selectionDataClosed, 'Current Language: ', dataLanguage, "Method used: ", methodData); //for debugging
  res.send('Selection saved!');
});

app.post('/save-selection-open', (req, res) => {
  console.log("got data - save-selection-open:", req.body);
  dataOpen = req.body.data;
  dataLanguage = req.body.language;
  methodData = "Open Ended Data Entry"
  console.log('Received Selection:', dataOpen, 'Current Language: ', dataLanguage, "Method used: ", methodData); //for debugging
  res.send('Selection saved!');
});

app.post('/save-selection-open-hybrid', (req, res) => {
  console.log("got data - save-selection-open-hybrid:", req.body);
  dataOpen = req.body.data;
  dataLanguage = req.body.language;
  methodData = "Open Ended Hybrid Data Entry"
  console.log('Received Selection:', dataOpen, 'Current Language: ', dataLanguage, "Method used: ", methodData); //for debugging
  res.send('Selection saved!');
});

app.get('/data', (req, res) => {
  switch(methodData){
    case "Closed Ended Data Entry": group_sql = "Group1"; break;
    case "Open Ended Hybrid Data Entry": group_sql = "Group2"; break;
    case "Closed Ended Hybrid Data Entry": group_sql = "Group3"; break;
    case "Open Ended Data Entry": group_sql = "Group4"; break;  
  };
  if(dataLanguage!= "en"){inputSource = "deeplx"}else{inputSource= "user"};
  switch (methodData) {
    case "Closed Ended Data Entry": {
      insertDataClosed();
      console.log("case: closed data");
      res.send("Data inserted successfully" )
      break;
    }
    case "Closed Ended Hybrid Data Entry": {
      insertDataClosed();
      console.log("case: closed hybrid data");
      res.send("Data inserted successfully: ")
      break;
    }
    case "Open Ended Data Entry": {
      insertDataOpen();
      console.log("case: open data");
      res.send("Data inserted successfully: ")
      break;
    }
    case "Open Ended Hybrid Data Entry": {
      insertDataOpen();
      console.log("case: open hybrid data");
      res.send("Data inserted successfully: ")
      break;
    }
    default: {
      res.send("No Data to insert");
      console.log("No Data to insert");
      break;
    }
  }

});

app.delete('/clearMap', (req, res) => {
  selectionDataClosed.clear();
  res.status(204).send();
});

app.delete('/deleteWord', (req, res) => {
  const key = req.body.button;

  if (selectionDataClosed.has(key)) {
    selectionDataClosed.delete(key);
      res.status(204).send();
  } else {
      res.status(404).send('Value does not exist');
  }
});

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
    headers: db_headers
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
    if(i == keys.length - 1){
      closedQuery += `
      hhh:Behaviour-${habituuid} rdf:type owl:NamedIndividual,
                    hhh:${keys[i]} ; 
                              hhh:partOf hhh:ExperimentalSetting-${habituuid};
                              hhh:id "${habituuid}" ;
                              hhh:language "${dataLanguage}"^^rdf:langString;
                              hhh:source "${inputSource}"^^rdfs:Literal;
                              hhh:value "${await translate(selectionDataClosed.get(keys[i]),"en", dataLanguage)}".
                              `;
      break;
    }else{
      closedQuery += `
        hhh:Behaviour-${habituuid} rdf:type owl:NamedIndividual,
                    hhh:${keys[i]} ; 
                              hhh:partOf hhh:ExperimentalSetting-${habituuid};
                              hhh:id "${habituuid}" ;
                              hhh:language "${dataLanguage}"^^rdf:langString;
                              hhh:source "${inputSource}"^^rdfs:Literal;
                              hhh:value "${await translate(selectionDataClosed.get(keys[i]), "en", dataLanguage)}".
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
    headers: db_headers
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
                          hhh:value "${await translate(dataOpen, "en", dataLanguage)}".
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
