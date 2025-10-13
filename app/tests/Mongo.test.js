import { test } from 'node:test';
import assert from 'node:assert/strict';
import { connect, disconnect } from '../models/survey.js';


async function canReachMongo() {
  // Attempt to connect quickly and list collections
  try {
    const db = await connect();
    await db.listCollections().toArray();
    await disconnect();
    return { ok: true };
  } catch (e) {
    return { ok: false, error: e?.message || String(e) };
  }
}

test('Mongo connect + CRUD (integration)', async (t) => {
  const ping = await canReachMongo();
  if (!ping.ok) {
    const host = process.env.MONGO_HOST || 'localhost';
    const port = process.env.MONGO_PORT || '27017';
    const user = process.env.MONGO_USER || 'admin';
    const dbName = process.env.MONGO_DB || 'surveyjs';
    
    // Skip test if MongoDB is not available rather than failing
    if (ping.error && (ping.error.includes('Authentication failed') || ping.error.includes('ECONNREFUSED'))) {
      return t.skip(`MongoDB not available at mongodb://${user}:***@${host}:${port}/ (db=${dbName}). Error: ${ping.error}`);
    }
    
    assert.fail(`Mongo not reachable at mongodb://${user}:***@${host}:${port}/ (db=${dbName}). Error: ${ping.error}`);
  }

  let db;
  try {
    db = await connect();
    
    // Prepare minimal survey doc and result doc
    const surveyId = 'unit-test-survey';
    await db.collection('surveys').deleteMany({ id: surveyId });
    await db.collection('surveys').insertOne({ id: surveyId, title: 'Test Survey', json: { pages: [] } });

    const loaded = await db.collection('surveys').findOne({ id: surveyId });
    assert.ok(loaded, 'Survey not found after insertion');
    assert.strictEqual(loaded.id, surveyId);

    const resDoc = { surveyId, data: { a: 1 }, submittedAt: new Date(), userId: 'mongo-test-user' };
    const ins = await db.collection('results').insertOne(resDoc);
    assert.ok(ins.insertedId, 'Failed to insert result document');

    const got = await db.collection('results').findOne({ _id: ins.insertedId });
    assert.ok(got, 'Result document not found after insertion');
    assert.strictEqual(got.userId, 'mongo-test-user');

    // Clean up test data
    await db.collection('surveys').deleteMany({ id: surveyId });
    await db.collection('results').deleteOne({ _id: ins.insertedId });
  } finally {
    if (db) {
      await disconnect();
    }
  }
});
