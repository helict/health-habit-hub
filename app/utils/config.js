import dotenv from 'dotenv';

dotenv.config();

const config = {
  port: process.env.PORT || 3000,
  db: {
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'defaultUser',
    password: process.env.DB_PASSWORD || 'defaultPassword',
    database: process.env.DB_NAME || 'defaultDatabase',
    protocol: process.env.DB_PROTOCOL || 'http',
    dbPort: process.env.DB_PORT || 5432,
  },
  getDbEndpoint: function () {
    return `${this.db.protocol}://${this.db.host}:${this.db.port}/${this.db.name}`;
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
