import { test } from 'node:test';
import assert from 'node:assert/strict';
import { config } from '../utils/config.js';
import { Neo4jDbClient } from '../utils/Neo4jDatabase.js';
import neo4j from 'neo4j-driver';

function getNeo4jConfig() {
  // Prefer host-local defaults unless explicitly overridden by env
  const uri = process.env.NEO4J_URI || 'bolt://localhost:7687';
  const user = process.env.NEO4J_USER || 'neo4j';
  const password = process.env.NEO4J_PASSWORD || 'neo4j_password_change_me';
  return { uri, user, password };
}

async function canConnectBolt() {
  const { uri, user, password } = getNeo4jConfig();
  try {
    const driver = neo4j.driver(uri, neo4j.auth.basic(user, password), { connectionTimeout: 5000 });
    const session = driver.session();
    await session.run('RETURN 1');
    await session.close();
    await driver.close();
    return { ok: true };
  } catch (e) {
    return { ok: false, error: e?.message || String(e) };
  }
}

test('Neo4jDbClient constructs', async () => {
  const testConfig = { ...config, neo4j: { ...config.neo4j, uri: getNeo4jConfig().uri, user: getNeo4jConfig().user, password: getNeo4jConfig().password } };
  const client = new Neo4jDbClient(testConfig);
  assert.ok(client);
  await client.close();
});

test('Neo4jDbClient insertDonateData (integration)', async () => {
  const ping = await canConnectBolt();
  if (!ping.ok) {
    const { uri, user } = getNeo4jConfig();
    assert.fail(`Neo4j not reachable at ${uri} (user=${user}). Error: ${ping.error}`);
  }

  // Use localhost Bolt for tests
  const testConfig = { ...config, graphBackend: 'neo4j', neo4j: { ...config.neo4j, uri: getNeo4jConfig().uri, user: getNeo4jConfig().user, password: getNeo4jConfig().password } };
  const client = new Neo4jDbClient(testConfig);
  const userId = 'neo4j-test-user-e2e';

  const sample = {
    inputValue: 'Testing a habit end-to-end.',
    language: 'en',
    habitStrength: '3',
    experimentGroup: { closedTask: true, closedDescription: true },
    contexts: [
      { name: 'Behavior', value: 'test behavior' },
      { name: 'TimeReference', value: 'noon' },
    ],
  };

  await client.insertDonateData(sample, userId);
  await client.close();

  // Verify via direct driver query
  const { uri, user, password } = getNeo4jConfig();
  const driver = neo4j.driver(uri, neo4j.auth.basic(user, password));
  const session = driver.session();
  try {
    const res = await session.run(
      'MATCH (d:Resource:hhh__Donor) WHERE any(x IN d.hhh__userId WHERE x = $uid) RETURN d LIMIT 1',
      { uid: userId }
    );
    assert.ok(res.records.length === 1, 'Donor not found');
  } finally {
    await session.close();
    await driver.close();
  }
});
