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

const app = express();
const port = config.port;

// SPARQL client config
// eslint-disable-next-line no-unused-vars
const sparqlClient = new SparqlDatabaseClient(config);

// Use bodyParser and express-recaptcha module
app.use(bodyParser.urlencoded({ extended: true }));

// Configure the reCAPTCHA module with your own keys
const recaptcha = new Recaptcha(
  '6Lc_WPEpAAAAAFmAbljvtUq2lX3Iekior1r3qr7l',
  '6Lc_WPEpAAAAAJKIbXTBmYBGKsZeay4ANUykwh7m',
);
app.use(recaptcha.middleware.render);

// Middleware for parsing form data in the request body
app.use(jsonBodyParser);

// Middleware for serving static files
app.use(staticFileMiddleware);




// Either sets req.lang to the already set route language parameter or gets the preferred browser language. Default value is 'en'. 
app.use('/:lng(de|en|ja)?/', (req, res, next) => {
  //console.log('Route language parameter:', req.params.lng);
  req.lang = 'en';

  if (req.params.lng) {
    req.lang = req.params.lng;
  } else {
    const lang = req.acceptsLanguages('de', 'ja', 'en');
    //console.log('Accepted browser language:', lang);

    if (lang) {
      req.lang = lang;
    } 
  
  }
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

// Intercepts all calls of '/' and checks whether a language (req.lang) is already set. If not, this parameter is set.
app.use( (req, res, next) => {
  if (req.url.startsWith('/' + req.lang + '/')) {
    next();
  } else {
    res.redirect(301, path.join('/', req.lang, req.url));
  }
});

/* eslint-disable */

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
      console.error('Error processing form:', error.message);
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
