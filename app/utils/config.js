import dotenv from 'dotenv';

dotenv.config();

const config = {
  path: process.env.PATH || './',
  port: process.env.PORT || 3000,
  recaptcha: {
    siteKey: process.env.RECAPTCHA_SITEKEY || '',
    secretKey: process.env.RECAPTCHA_SECRETKEY || '',
    useRecaptchaDomain: process.env.RECAPTCHA_USE_RECAPTCHA_DOMAIN || false,
  },
  db: {
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'defaultUser',
    password: process.env.DB_PASSWORD || 'defaultPassword',
    path: process.env.DB_PATH || 'defaultDatabase',
    protocol: process.env.DB_PROTOCOL || 'http',
    port: process.env.DB_PORT || 5432,
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
