// configuration/experimentConfig.js
import { MongoClient } from 'mongodb';
import { ALL_EXPERIMENT_GROUPS } from '../models/experimentGroup.js';

const dbName = process.env.MONGO_DB || 'surveyjs';

// build connection string from MONGO_URL or single ENV vars (no docker-compose change needed)
const mongoUrl = process.env.MONGO_URL || (() => {
  const user = process.env.MONGO_USER || 'admin';
  const pass = process.env.MONGO_PASSWORD || 'admin';
  const host = process.env.MONGO_HOST || 'localhost';
  const db   = dbName;
  const u = encodeURIComponent(user);
  const p = encodeURIComponent(pass);
  return `mongodb://${u}:${p}@${host}:27017/${db}?authSource=admin`;
})();

let client = null;
let db = null;
let connected = false;

async function connectWithRetry(retries = 6, baseDelayMs = 500) {
  if (connected && db) return;
  client = client || new MongoClient(mongoUrl);
  for (let i = 0; i < retries; i++) {
    try {
      await client.connect();
      db = client.db(dbName);
      connected = true;
      return;
    } catch (err) {
      const delay = baseDelayMs * (i + 1);
      console.warn(`Mongo connect attempt ${i + 1} failed, retrying in ${delay}ms...`, err.message);
      await new Promise((r) => setTimeout(r, delay));
    }
  }
  throw new Error('Could not connect to MongoDB after retries');
}

// load config document (returns { enabledGroups: [...], useAllGroups: bool })
export async function loadExperimentConfig() {
  await connectWithRetry();
  const col = db.collection('app_config');
  const doc = await col.findOne({ _id: 'experimentConfig' });
  if (!doc) {
    // default: all groups enabled
    return {
      enabledGroups: ALL_EXPERIMENT_GROUPS.map((g) => g.toString()),
      useAllGroups: false,
    };
  }
  return {
    enabledGroups: Array.isArray(doc.enabledGroups) ? doc.enabledGroups : [],
    useAllGroups: !!doc.useAllGroups,
  };
}

// persist config: { enabledGroups: [...], useAllGroups: bool }
export async function updateExperimentConfig({ enabledGroups = [], useAllGroups = false }) {
  await connectWithRetry();
  const col = db.collection('app_config');
  const doc = {
    enabledGroups: Array.isArray(enabledGroups) ? enabledGroups : [],
    useAllGroups: !!useAllGroups,
    updatedAt: new Date(),
  };
  await col.updateOne({ _id: 'experimentConfig' }, { $set: doc }, { upsert: true });
  return doc;
}
