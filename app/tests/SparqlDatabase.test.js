import { test } from 'node:test';
import assert from 'node:assert';
import { DbClient } from '../utils/SparqlDatabase.js';
import SparqlClient from 'sparql-http-client';
import { ExperimentGroup } from '../models/experimentGroup.js';

const sparqlClientTestConfig = {
  getDbEndpoint: () => 'http://localhost:3030/hhh',
  db: {
    user: 'admin',
    password: 'admin',
  },
  getDbHeader: () => [
    ['host', 'localhost'],
    ['port', 3030],
    ['path', '/hhh'],
  ],
};

test('Create instance of DbClient', () => {
  const dbClient = new DbClient(sparqlClientTestConfig);
  assert(dbClient instanceof DbClient);
  assert(dbClient.client instanceof SparqlClient);
  assert.strictEqual(
    dbClient.client.query.endpoint.updateUrl,
    'http://localhost:3030/hhh',
  );
  // Base64 encoded 'admin:admin'
  assert.strictEqual(
    dbClient.client.query.endpoint.headers.get('authorization'),
    'Basic YWRtaW46YWRtaW4=',
  );
  assert.strictEqual(
    dbClient.client.query.endpoint.headers.get('host'),
    'localhost',
  );
  assert.strictEqual(
    dbClient.client.query.endpoint.headers.get('port'),
    '3030',
  );
});

// Skip test, because test case is only partially completed
test.skip('Insert open data', async () => {
  const openExperimentGroup = new ExperimentGroup(false, false);
  const data = {
    //   language: 'en',
    language: 'de',
    source: 'user',
    //   inputValue: 'I eat a banana',
    inputValue: 'Ich esse eine Pflaume',
  };
  const dbClient = new DbClient(sparqlClientTestConfig);
  await dbClient.insertDonateData(openExperimentGroup, data);
});

// Skip test, because test case is only partially completed
test.skip('Insert closed data', async () => {
  const openExperimentGroup = new ExperimentGroup(true, true);
  const data = {
    //   language: 'en',
    language: 'de',
    source: 'user',
    //   inputValue: 'I eat a banana',
    inputValue: 'Morgens esse ich einen Kuchen.',
    contexts: [
      {
        name: 'Behavior',
        value: 'esse',
      },
      {
        name: 'Time',
        value: 'Morgens',
      },
    ],
  };
  const dbClient = new DbClient(sparqlClientTestConfig);
  await dbClient.insertDonateData(openExperimentGroup, data);
});
