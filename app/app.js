import express from 'express';
import bodyParser from 'body-parser';
import Recaptcha from 'express-recaptcha'; // Import the express-recaptcha module

import sparqlClient from 'sparql-http-client';
import {v4 as uuid} from 'uuid';
import path, {dirname} from 'path';
import {translate} from 'deeplx';
import {fileURLToPath} from "url";

import {staticFileMiddleware} from './middleware/staticFileMiddleware.js';
import {jsonBodyParser} from './middleware/requestParser.js';
import {config} from "./EnvManager.js";

import donateRouter from "./routers/donateRouter.js";
import aboutRouter from "./routes/aboutRouter.js";

const app = express();
const port = config.port;

const db_user = config.db.user
const db_pass = config.db.password
const db_proto = config.db.protocol
const db_host = config.db.host
const db_port = config.db.dbPort
const db_name = config.db.name
const db_endpoint = config.getDbEndpoint()
const db_headers = config.getDbHeader()

const __dirname = dirname(fileURLToPath(import.meta.url));

// Use bodyParser and express-recaptcha module
app.use(bodyParser.urlencoded({ extended: true }));

// Configure the reCAPTCHA module with your own keys
const recaptcha = new Recaptcha('6Lc_WPEpAAAAAFmAbljvtUq2lX3Iekior1r3qr7l', '6Lc_WPEpAAAAAJKIbXTBmYBGKsZeay4ANUykwh7m');
app.use(recaptcha.middleware.render);

// Middleware for parsing form data in the request body
app.use(jsonBodyParser);

// Middleware for serving static files
app.use(staticFileMiddleware);

let selectionDataClosed = new Map();
let dataOpen;
let dataLanguage;
let inputSource;
let group_sql;

// Routes
app.get("/", (req, res) => {
  res.redirect(301, "/donate");
});
app.use("/donate", donateRouter);
app.use('/about.html', aboutRouter);

// SPARQL Connection
async function insertDataClosed() {
  // Code for data processing...
}

async function insertDataOpen() {
  // Code for data processing...
}

// Route for the contact form with reCAPTCHA verification
app.post('/submit-form', recaptcha.middleware.verify, async (req, res) => {
    // Verify the captcha
    if (!req.recaptcha.error) {
        // Captcha verification passed successfully
        // Perform your further logic here
        try {
            await insertDataClosed(); // Example of a function for data processing
            await insertDataOpen(); // Example of a function for data processing
            res.send('Form submitted successfully!');
        } catch (error) {
            console.error("Error processing form:", error.message);
            res.status(500).send('Internal Server Error');
        }
    } else {
        // Captcha verification failed
        res.status(400).send('Captcha verification failed');
    }
});

app.listen(port, () => {
  console.log(`Server is running on http://app.localhost`);
});
