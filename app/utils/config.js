import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

// Get the directory of this file
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load .env from project root (two levels up from utils/)
dotenv.config({ path: path.resolve(__dirname, '../../.env') });

const config = {
  path: process.env.PATH || './',
  port: process.env.PORT || 3000,
  recaptcha: {
    siteKey: (process.env.RECAPTCHA_SITEKEY || '').trim(),
    secretKey: (process.env.RECAPTCHA_SECRETKEY || '').trim(),
    useRecaptchaDomain: process.env.RECAPTCHA_USE_RECAPTCHA_DOMAIN === 'true',
  },
  db: {
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'defaultUser',
    password: process.env.DB_PASSWORD || 'defaultPassword',
    path: process.env.DB_PATH || 'defaultDatabase',
    protocol: process.env.DB_PROTOCOL || 'http',
    port: process.env.DB_PORT || 5432,
  },
  graphBackend: process.env.GRAPH_BACKEND || 'fuseki', // 'fuseki' | 'neo4j'
  neo4j: {
    uri: process.env.NEO4J_URI || 'bolt://neo4j:7687',
    user: process.env.NEO4J_USER || 'neo4j',
    password: process.env.NEO4J_PASSWORD || 'password',
  },
  translateApi: {
    host: process.env.TRANSLATE_HOST || 'localhost',
    port: process.env.TRANSLATE_PORT || '5000',
    path: process.env.TRANSLATE_PATH || '/translate',
    protocol: process.env.TRANSLATE_PROTOCOL || 'http'
  },
  getDbEndpoint: function () {
    return `${this.db.protocol}://${this.db.host}:${this.db.port}/${this.db.path}`;
  },
   mail: {
    host: process.env.MAIL_HOST,
    port: parseInt(process.env.MAIL_PORT, 10),
    user: process.env.MAIL_USER,
    pass: process.env.MAIL_PASS,
    from: process.env.MAIL_FROM,
    receiver: process.env.MAIL_RECEIVER
  },
  getDbHeader: function () {
    return [
      ['host', this.db.host],
      ['port', this.db.port],
      ['path', `/${this.db.name}`],
    ];
  },
  getTranslateApiEndpoint: function () {
    return `${this.translateApi.protocol}://${this.translateApi.host}:${this.translateApi.port}${this.translateApi.path}`;
  }
};

export { config };
