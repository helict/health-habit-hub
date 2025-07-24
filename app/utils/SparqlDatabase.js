import SparqlClient from 'sparql-http-client';
import fetch from 'node-fetch';
import { v4 as uuid } from 'uuid';
import { config } from './config.js';

// function to translate text using LibreTranslate API
async function translate(text, from, to) {
  const response = await fetch(config.getTranslateApiEndpoint(), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      q: text,
      source: from,
      target: to,
      format: "text",
      alternatives: 0
    }),
  });

  if (response.ok) {
    const translation = await response.json();
    return translation.translatedText;
  }

  // TODO: Implement proper error handling
  throw new Error(`Translation failed: ${response.statusText}`);
}

class ExperimentalSetting {
  id;
  description;
  task;
  group;

  constructor(setting) {
    this.id = uuid();
    // TODO: Refactor constructor
    this.description = setting.closedDescription ? "closed" : "open";
    this.task = setting.closedTask ? "closed" : "open";
    if (this.isClosedTaskOpenDescription()) this.group = "Group1";
    else if (this.isClosedTaskClosedDescription) this.group = "Group2";
    else if (this.isOpenTaskClosedDescription) this.group = "Group3";
    else if (this.isOpenTaskOpenDescription) this.group = "Group4";
  }

  isClosedTaskClosedDescription() {
    return (this.task === "closed") && (this.description === "closed");
  }

  isClosedTaskOpenDescription() {
    return (this.task === "closed") && (this.description === "open");
  }

  isOpenTaskOpenDescription() {
    return (this.task === "open") && (this.description === "open");
  }

  isOpenTaskClosedDescription() {
    return (this.task === "open") && (this.description === "closed");
  }
}

class Donor {
  id;
  donation;
  constructor(donation) {
    this.id = uuid();
    this.donation = donation;
  }
}

class Label {
  id;
  type;
  value;
  data;

  constructor(type, value, data) {
    this.id = uuid();
    this.type = type;
    this.value = value;
    this.data = data;
  }
}

class Donation {
  id;
  value;
  labels;
  language;
  source;
  translation;
  habitStrength;

  constructor(value, language, labels, source, habitStrength) {
    this.id = uuid();
    this.value = value;
    this.language = language;
    // TODO: Refactor label constructor
    this.labels = labels.map(label => 
      new Label({
        "TimeReference": "context",
        "PhysicalSetting": "context",
        "People": "context",
        "InternalState": "context",
        "PriorBehavior": "context",
        "Behavior": "behavior"
      }[label.name],
      label.name,
      label.value
    ));
    this.source = source;
    this.habitStrength = habitStrength;
  }

  hasLabels() {
    return this.labels && (this.labels.length > 0);
  }

  // TODO: Refactor
  async translate(targetLanguage) {
    // Translation functions
    const translateValue = async () => 
      await translate(this.value, this.language, targetLanguage);
    const translateLabels = async () =>
      await Promise.all(this.labels.map(async (label) =>
        await translate(label.data, this.language, targetLanguage)));
    
    // Perform translation
    const translatedValue = await translateValue();
    const translatedLabels = this.hasLabels() ? await translateLabels() : [];
    const labelsCopy = this.labels.map((label, index) => Object.assign({name: label.value, value: translatedLabels[index]}));

    // Remember translated donation
    this.translation = new Donation(translatedValue, targetLanguage, labelsCopy, "translation", this.habitStrength);
    return this.translation;
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

  async insertDonateData(data, userId) {
    // TODO: Move to config/env
    const NORMALIZE_LANG = 'en';

    // Input data
    const mustTranslate = !data.language.toLowerCase().startsWith(NORMALIZE_LANG);
    const experimentalSetting = new ExperimentalSetting(data.experimentGroup);
    const donation = new Donation(data.inputValue, data.language, data.contexts, userId, parseInt(data.habitStrength, 10));
    const donor = new Donor(donation);
    let insertQuery = "";

    if (mustTranslate) {
      await donation.translate(NORMALIZE_LANG);
    }

    // TOOO: Remove (check delay)
    new Promise(r => setTimeout(r, 4000)).then(console.debug(donation));

    // Create SPARQL query
    insertQuery = this.addExperimentalSetting(insertQuery, experimentalSetting);
    insertQuery = this.addHabit(insertQuery, donation);
    insertQuery = this.addDonor(insertQuery, donor, userId);

    if (donation.translation) {
      insertQuery = this.addHabit(insertQuery, donation.translation);
    }
   
    if (donation.hasLabels()) {
      insertQuery = this.addContext(insertQuery, donation, experimentalSetting);
      insertQuery = this.addBehavior(insertQuery, donation, experimentalSetting);
    }

    insertQuery = this.addEnvelope(insertQuery);

    // Execute SPARQL query
    console.debug(insertQuery);
    await this.insertData(insertQuery);
  }

  addEnvelope(query) {
    return `
      PREFIX hhh: <http://example.com/hhh#>
      PREFIX owl: <http://www.w3.org/2002/07/owl#>
      PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
      PREFIX xml: <http://www.w3.org/XML/1998/namespace>
      PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      BASE <http://www.w3.org/2002/07/owl#>
    
      INSERT DATA {
    ` + query + "}"
  }

  addExperimentalSetting(query, experimentalSetting) {
    return query += `
      hhh:ExperimentalSetting-${experimentalSetting.id} rdf:type owl:NamedIndividual ,
        hhh:${experimentalSetting.group}.
    `;
  }

  addDonor(query, donor, userId) {
    return query += `
      hhh:Donor-${donor.id} rdf:type owl:NamedIndividual , hhh:Donor ;
        hhh:donates hhh:Habit-${donor.donation.id} ; hhh:userId "${userId}"^^xsd:token ;
        hhh:id "${donor.id}"^^xsd:token .
    `;
  }

  addHabit(query, donation) {
    const behaviors = donation.labels
      .filter(label => label.type === "behavior");
    const behaviorStatement = ((behaviors && behaviors.length > 0) ? `hhh:hasBehavior ${behaviors.map(behavior => `hhh:Behavior-${behavior.id}`).join(", ")} ;` : "");
    return query += `
      hhh:Habit-${donation.id} rdf:type owl:NamedIndividual , hhh:Habit ;
        ${behaviorStatement}
        hhh:habitStrength "${donation.habitStrength}"^^xsd:integer ;
        hhh:id "${donation.id}"^^xsd:token ;
        hhh:language "${donation.language}" ;
        hhh:source "${donation.source}"^^rdfs:Literal ;
        hhh:value "${donation.value}" .
    `;
  }

  addContext(query, donation, experimentalSetting) {
    // TODO: Refactor
    if (donation.translation) {
      return query 
        + this._appendContext(donation, donation.translation, experimentalSetting)
        + this._appendContext(donation.translation, donation, experimentalSetting);
    }
    
    return query + this._appendContext(donation, donation.translation, experimentalSetting);
  }

  // TODO: Refactor
  _appendContext(donation, translatedDonation, experimentalSetting) {
    return donation.labels
      .filter(label => label.type === "context")
      .map(context => {
        const translation = translatedDonation 
          ? translatedDonation.labels
            .filter(label => label.type === "context")
            .find(label => label.value === context.value)
          : undefined;
        const translationStatement = translation ? `hhh:hasTranslation hhh:Context-${translation.id} ;` : "";
        return `
          hhh:Context-${context.id} rdf:type owl:NamedIndividual , hhh:${context.value};
            ${translationStatement}
            hhh:partOf hhh:ExperimentalSetting-${experimentalSetting.id} ;
            hhh:id "${context.id}"^^xsd:token ;
            hhh:language "${donation.language}" ;
            hhh:source "${donation.source}"^^rdfs:Literal ;
            hhh:value "${context.data}" .
          `;
      })
      .join("");
  }

  addBehavior(query, donation, experimentalSetting) {
    // TODO: Refactor
    if (donation.translation) {
      return query 
        + this._appendBehavior(donation, donation.translation, experimentalSetting)
        + this._appendBehavior(donation.translation, donation, experimentalSetting);
    }
    
    return query + this._appendBehavior(donation, donation.translation, experimentalSetting);
  }

  // TODO: Refactor
  _appendBehavior(donation, translatedDonation, experimentalSetting) {
    const contextStatement = donation.labels
      .filter(label => label.type === "context")
      .map(context => `hhh:Context-${context.id}`)
      .join(" , ");
    return donation.labels
      .filter(label => label.type === "behavior")
      .map(behavior => {
        const translation = translatedDonation 
          ? translatedDonation.labels
            .filter(label => label.type === "behavior")
            .find(label => label.value === behavior.value)
          : undefined;
        const translationStatement = translation ? `hhh:hasTranslation hhh:Behavior-${translation.id} ;` : "";
        return `
          hhh:Behavior-${behavior.id} rdf:type owl:NamedIndividual , hhh:Behavior;
            hhh:hasContext ${contextStatement} ;
            ${translationStatement}
            hhh:partOf hhh:ExperimentalSetting-${experimentalSetting.id} ;
            hhh:id "${behavior.id}"^^xsd:token ;
            hhh:language "${donation.language}" ;
            hhh:source "${donation.source}"^^rdfs:Literal ;
            hhh:value "${behavior.data}" .
          `;
      })
      .join("");
  }
}

export { DbClient };
