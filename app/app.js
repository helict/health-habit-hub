import path from 'path';
import express from 'express';
import bodyParser from 'body-parser';
import { RecaptchaV2 as Recaptcha } from 'express-recaptcha'; // Import the express-recaptcha module

import { config } from './utils/config.js';
import { staticFileMiddleware } from './middleware/staticFileMiddleware.js';
import { jsonBodyParser } from './middleware/requestParser.js';
import { SparqlDatabaseClient } from './utils/SparqlDatabase.js';

// Express config
import donateRouter from './routes/donateRouter.js';
import aboutRouter from './routes/aboutRouter.js';
import demoRouter from './routes/demoRouter.js';
import thanksRouter from './routes/thanksRouter.js';

const app = express();
const port = config.port;

// SPARQL client config
// eslint-disable-next-line no-unused-vars
const sparqlClient = new SparqlDatabaseClient(config);

// Use bodyParser and express-recaptcha module
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json()); // Added to parse JSON bodies

// Configure the reCAPTCHA module with your own keys
const recaptcha = new Recaptcha(
  '6Lc_WPEpAAAAAFmAbljvtUq2lX3Iekior1r3qr7l',
  '6Lc_WPEpAAAAAJKIbXTBmYBGKsZeay4ANUykwh7m'
);
app.use(recaptcha.middleware.render);

// Middleware for parsing form data in the request body
app.use(jsonBodyParser);

// Middleware for serving static files
app.use(staticFileMiddleware);

// Middleware to add reCAPTCHA to the context
app.use((req, res, next) => {
  res.locals.recaptcha = recaptcha.render();
  next();
});

// Either sets req.lang to the already set route language parameter or gets the preferred browser language. Default value is 'en'. 
app.use('/:lng(de|en|ja)?/', (req, res, next) => {
  req.lang = 'en';

  if (req.params.lng) {
    req.lang = req.params.lng;
  } else {
    const lang = req.acceptsLanguages('de', 'ja', 'en');
    if (lang) {
      req.lang = lang;
    }
  }
  res.locals.currentLanguage = req.lang;
  console.log('Application language:', req.lang);
  next();
});

// Routes
// Redirects all requests to '/donate' if the language parameter (lng) is already set
app.get('/:lng(de|en|ja)/', (req, res) => {
  res.redirect(301, '/' + req.lang + '/donate');
});

app.use('/:lng(de|en|ja)/donate', donateRouter);
app.use('/:lng(de|en|ja)/about', aboutRouter);
app.use('/:lng(de|en|ja)/demo', demoRouter);
app.use('/:lng(de|en|ja)/thanks', thanksRouter);

// Intercepts all calls of '/' and checks whether a language (req.lang) is already set. If not, this parameter is set.
app.use((req, res, next) => {
  if (req.url.startsWith('/' + req.lang + '/')) {
    next();
  } else {
    res.redirect(301, path.join('/', req.lang, req.url));
  }
});

/* eslint-disable */

// Route for the contact form with reCAPTCHA verification
app.post('/:lng(de|en|ja)/submit-form', recaptcha.middleware.verify, async (req, res) => {
  if (!req.recaptcha.error) {
    try {
      // Replace these with your actual data processing functions
      await insertDataClosed(); // Example of a function for data processing
      await insertDataOpen(); // Example of a function for data processing
      res.send('Form submitted successfully!');
    } catch (error) {
      console.error('Error processing form:', error.message);
      res.status(500).send('Internal Server Error');
    }
  } else {
    console.error('Captcha verification failed:', req.recaptcha.error);
    res.status(400).send('Captcha verification failed');
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://app.localhost`);
});
