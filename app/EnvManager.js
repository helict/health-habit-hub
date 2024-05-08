require('dotenv').config();

const config = {
    port: process.env.PORT || 3000,
    db: {
        host: process.env.DB_HOST,
        port: process.env.PORT,
        user: process.env.DB_USER,
        password: process.env.DB_PASSWORD,
        database: process.env.DB_NAME,
        protocol: process.env.DB_PROTOCOL,
        dbPort: process.env.DB_PORT
    },
    getDbEndpoint: function () {
        return `${this.db.protocol}://${this.db.host}:${this.db.port}/${this.db.name}`;
    },

    getDbHeader: function (){
        return [
            ["host", this.db.host],
            ["port", this.db.port],
            ["path", `/${this.db.name}`]
        ];
    }
};

module.exports = config;

