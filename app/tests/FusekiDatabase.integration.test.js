import { test } from 'node:test';
import assert from 'node:assert/strict';
import { DbClient } from '../utils/SparqlDatabase.js';


function getFusekiConfig() {
  const host = process.env.FUSEKI_HOST || 'localhost';
  const port = parseInt(process.env.FUSEKI_PORT || '3030', 10);
  const dataset = process.env.FUSEKI_DATASET || 'hhh';
  const user = process.env.FUSEKI_USER || 'admin';
  const password = process.env.FUSEKI_PASSWORD || 'admin';
  const endpoint = `http://${host}:${port}/${dataset}`;
  return { endpoint, host, port, dataset, user, password };
}

async function canReachFuseki() {
  const { endpoint } = getFusekiConfig();
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 5000);
    const res = await fetch(endpoint, { method: 'GET', signal: controller.signal });
    clearTimeout(timeout);
    return { ok: res.ok, status: res.status };
  } catch (e) {
    return { ok: false, error: e?.message || String(e) };
  }
}

test('Sparql DbClient constructs with test config', () => {
  const { endpoint, host, port, dataset, user, password } = getFusekiConfig();
  const cfg = {
    getDbEndpoint: () => endpoint,
    db: { user, password },
    getDbHeader: () => [ ['host', host], ['port', port], ['path', `/${dataset}`] ],
  };
  const c = new DbClient(cfg);
  assert.ok(c);
});

test('Insert and verify with Fuseki (integration)', async () => {
  const ping = await canReachFuseki();
  if (!ping.ok) {
    const { endpoint } = getFusekiConfig();
    const extra = ping.error ? `Error: ${ping.error}` : `HTTP ${ping.status}`;
    assert.fail(`Fuseki not reachable at ${endpoint}. ${extra}`);
  }

  const { endpoint, host, port, dataset, user, password } = getFusekiConfig();
  const cfg = {
    getDbEndpoint: () => endpoint,
    db: { user, password },
    getDbHeader: () => [ ['host', host], ['port', port], ['path', `/${dataset}`] ],
  };

  const client = new DbClient(cfg);
  const uid = 'fuseki-test-user-e2e';

  const data = {
    inputValue: 'Fuseki integration habit.',
    language: 'en',
    habitStrength: '2',
    experimentGroup: { closedTask: false, closedDescription: false },
    contexts: [ { name: 'Behavior', value: 'fuseki test behavior' } ],
  };

  await client.insertDonateData(data, uid);

  // Verify with a direct fetch to avoid connection hanging issues
  const queryEndpoint = `${endpoint}/query`;
  const SELECT = `
    PREFIX hhh: <http://example.com/hhh#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT ?d WHERE {
      ?d a hhh:Donor ; hhh:userId "${uid}"^^xsd:token ; hhh:donates ?h .
    } LIMIT 1`;

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 5000);
  
  try {
    const response = await fetch(queryEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/sparql-query',
        'Accept': 'application/sparql-results+json',
        'Authorization': `Basic ${Buffer.from(`${user}:${password}`).toString('base64')}`
      },
      body: SELECT,
      signal: controller.signal
    });
    
    assert.ok(response.ok, `SPARQL query failed: ${response.status} ${response.statusText}`);
    const result = await response.json();
    assert.ok(result.results && result.results.bindings.length > 0, 'Inserted donor not found in Fuseki');
  } finally {
    clearTimeout(timeout);
  }
});
