import { MongoClient, ObjectId } from 'mongodb';

const dbConfig = {
    host: process.env.MONGO_HOST || "localhost",
    port: process.env.MONGO_PORT || 27017,
    database: process.env.MONGO_DB,
    user: process.env.MONGO_USER,
    password: process.env.MONGO_PASSWORD
};

// TODO: export collection names
// TODO: disconnect from db

const url = `mongodb://${dbConfig.user}:${dbConfig.password}@${dbConfig.host}:${dbConfig.port}/`;
let db;

export async function connect() {
  if (db) {
    return db;
  }

  const client = new MongoClient(url);
  await client.connect();
  db = client.db(dbConfig.database);
  return db;
}

async function disconnect() {
    // TODO
}

export { ObjectId };