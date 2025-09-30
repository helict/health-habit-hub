import { test } from 'node:test';
import assert from 'node:assert';
import { DbClient } from '../utils/SparqlDatabase.js';
import SparqlClient from 'sparql-http-client';
import { ExperimentGroup } from '../models/experimentGroup.js';

const INTEGRATION = /^1|true$/i.test(process.env.ENABLE_INTEGRATION || '');

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
    'http://localhost:3030/hhh'
  );
  // Base64 encoded 'admin:admin'
  assert.strictEqual(
    dbClient.client.query.endpoint.headers.get('authorization'),
    'Basic YWRtaW46YWRtaW4='
  );
  assert.strictEqual(
    dbClient.client.query.endpoint.headers.get('host'),
    'localhost'
  );
  assert.strictEqual(
    dbClient.client.query.endpoint.headers.get('port'),
    '3030'
  );
});

test('Insert open data (integration)', async (t) => {
  if (!INTEGRATION) return t.skip('Integration disabled (set ENABLE_INTEGRATION=1)');
  const openExperimentGroup = new ExperimentGroup(false, false);
  const data = {
    language: 'en',
    source: 'user',
    inputValue: 'I eat a banana',
    experimentGroup: openExperimentGroup,
  };
  const dbClient = new DbClient(sparqlClientTestConfig);
  try {
    await dbClient.insertDonateData(data, 'sparql-open-test-user');
  } finally {
    if (dbClient && typeof dbClient.close === 'function') {
      await dbClient.close();
    }
  }
});

test('Insert closed data (integration)', async (t) => {
  if (!INTEGRATION) return t.skip('Integration disabled (set ENABLE_INTEGRATION=1)');
  const closedExperimentGroup = new ExperimentGroup(true, true);
  const data = {
    language: 'en',
    source: 'user',
    inputValue: 'In the morning I eat cake.',
    experimentGroup: closedExperimentGroup,
    contexts: [
      { name: 'Behavior', value: 'eat' },
      { name: 'TimeReference', value: 'morning' },
    ],
  };
  const dbClient = new DbClient(sparqlClientTestConfig);
  try {
    await dbClient.insertDonateData(data, 'sparql-closed-test-user');
  } finally {
    if (dbClient && typeof dbClient.close === 'function') {
      await dbClient.close();
    }
  }
});
