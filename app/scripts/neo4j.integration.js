import { config } from '../utils/config.js';
import { Neo4jDbClient } from '../utils/Neo4jDatabase.js';

// Minimal integration exercise for Neo4jDbClient
// - Uses language 'en' to avoid translation service dependency
// - Inserts a sample donation and exits on success

async function main() {
  // Ensure backend is set to neo4j for clarity (client doesn't depend on it)
  config.graphBackend = 'neo4j';

  const client = new Neo4jDbClient(config);

  const sample = {
    inputValue: 'I drink water after waking up.',
    language: 'en',
    habitStrength: '4',
    experimentGroup: { closedTask: true, closedDescription: false },
    contexts: [
      { name: 'TimeReference', value: 'in the morning' },
      { name: 'PhysicalSetting', value: 'at home' },
      { name: 'People', value: 'alone' },
      { name: 'InternalState', value: 'thirsty' },
      { name: 'PriorBehavior', value: 'after brushing teeth' },
      { name: 'Reasoning', value: 'for hydration' },
      { name: 'Behavior', value: 'drink water' },
    ],
  };

  const userId = 'neo4j-int-test-user';

  try {
    await client.insertDonateData(sample, userId);
    console.log('Neo4j integration insert completed without error.');
  } finally {
    await client.close();
  }
}

main().catch((err) => {
  console.error('Neo4j integration test failed:', err);
  process.exitCode = 1;
});
