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

test('insertDonateData links habits to experimental setting and preserves all four groups', async () => {
  const scenarios = [
    { group: new ExperimentGroup(true, false), expected: 'Group1' },
    { group: new ExperimentGroup(true, true), expected: 'Group2' },
    { group: new ExperimentGroup(false, true), expected: 'Group3' },
    { group: new ExperimentGroup(false, false), expected: 'Group4' },
  ];

  for (const { group, expected } of scenarios) {
    const dbClient = new DbClient(sparqlClientTestConfig);
    let capturedQuery = '';
    dbClient.insertData = async (query) => {
      capturedQuery = query;
    };

    await dbClient.insertDonateData(
      {
        language: 'en',
        source: 'user',
        inputValue: `habit for ${expected}`,
        habitStrength: '3',
        experimentGroup: group,
        contexts: [],
      },
      `sparql-unit-${expected.toLowerCase()}`
    );

    assert.match(
      capturedQuery,
      new RegExp(`hhh:ExperimentalSetting-[^\\s]+ rdf:type owl:NamedIndividual ,\\s+hhh:${expected}\\.`),
      `expected experimental setting to be typed as ${expected}`
    );
    assert.match(
      capturedQuery,
      /hhh:Habit-[^\s]+ rdf:type owl:NamedIndividual , hhh:Habit ;[\s\S]*?hhh:partOf hhh:ExperimentalSetting-[^\s]+ ;/,
      'expected habit to link directly to its experimental setting'
    );
  }
});
