import dotenv from 'dotenv';

dotenv.config();

const config = {
  path : process.env.PATH || './',
  port: process.env.PORT || 3000,
  recaptcha: {
    siteKey: process.env.RECAPTCHA_SITEKEY || '',
    secretKey: process.env.RECAPTCHA_SECRETKEY || '',
  },
  db: {
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'defaultUser',
    password: process.env.DB_PASSWORD || 'defaultPassword',
    path: process.env.DB_PATH || 'defaultDatabase',
    protocol: process.env.DB_PROTOCOL || 'http',
    port: process.env.DB_PORT || 5432,
  },
  getDbEndpoint: function () {
    return `${this.db.protocol}://${this.db.host}:${this.db.port}/${this.db.path}`;
  },

  getDbHeader: function () {
    return [
      ['host', this.db.host],
      ['port', this.db.port],
      ['path', `/${this.db.name}`],
    ];
  },
};

export { config };
