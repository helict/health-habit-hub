import sparqlClient from 'sparql-http-client';
import {translate} from 'deeplx';
import {config} from './config.js';

class SparqlClient {
    constructor() {
        this.client = new sparqlClient({
            updateUrl: config.getDbEndpoint(),
            user: config.db.user,
            password: config.db.password,
            headers: config.getDbHeader(),
        });
    }

    async insertData(query) {
        try {
            await this.client.query.update(query);
            console.log("Data inserted successfully");
        } catch (error) {
            console.debug(query);
            console.error("Error inserting data:", error.message);
        }
    }

    async insertDonateData(habituuid, ExperimentGroup, data, keys = []) {
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
                                            hhh:${ExperimentGroup.toString()}.
    `;

            if (ExperimentGroup.closedTask) {
                let i = 0;
                while (i < keys.length) {
                    query += `
      hhh:Behaviour-${habituuid} rdf:type owl:NamedIndividual,
                  hhh:${keys[i]} ;
                            hhh:partOf hhh:ExperimentalSetting-${habituuid};
                            hhh:id "${habituuid}" ;
                            hhh:language "${data.language}"^^rdf:langString;
                            hhh:source "${data.source}"^^rdfs:Literal;
                            hhh:value "${await translate(
                        data.get(keys[i]),
                        "en",
                        data.language
                    )}".
      `;
                    i++;
                }
            } else {
                query += `
      hhh:Behaviour-${habituuid} rdf:type owl:NamedIndividual,
                  hhh:Behaviour ;
                            hhh:partOf hhh:ExperimentalSetting-${habituuid};
                            hhh:id "${habituuid}" ;
                            hhh:language "${data.language}"^^rdf:langString;
                            hhh:source "${data.source}"^^rdfs:Literal;
                            hhh:value "${await translate(
                    data,
                    "en",
                    data.language
                )}".
    `;
            }

            query += `}`;

            await this.insertData(query);
    }


}

export {SparqlClient};