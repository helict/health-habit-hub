import { MongoClient, ObjectId } from 'mongodb';
import dotenv from 'dotenv';
import path from 'path';

dotenv.config({ path: path.resolve('../.env') });

const dbConfig = {
    host: process.env.MONGO_HOST || "localhost",
    port: process.env.MONGO_PORT || 27017,
    database: process.env.MONGO_DB,
    user: process.env.MONGO_USER,
    password: process.env.MONGO_PASSWORD,
    authSource: process.env.MONGO_AUTH_SOURCE || 'admin'
};

const url = `mongodb://${dbConfig.user}:${dbConfig.password}@${dbConfig.host}:${dbConfig.port}/?authSource=${dbConfig.authSource}`;
let db;
let client;

export async function connect() {
  if (db) {
    return db;
  }

  client = new MongoClient(url, {
    serverSelectionTimeoutMS: parseInt(process.env.MONGO_SERVER_SELECTION_TIMEOUT_MS || '5000', 10),
    socketTimeoutMS: parseInt(process.env.MONGO_SOCKET_TIMEOUT_MS || '5000', 10),
  });
  await client.connect();
  db = client.db(dbConfig.database);
  return db;
}

export async function disconnect() {
  try {
    if (client) await client.close();
  } finally {
    client = undefined;
    db = undefined;
  }
}

export { ObjectId };
