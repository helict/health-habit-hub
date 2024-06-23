import express from 'express';
import bodyParser from 'body-parser';
import { RecaptchaV2 as Recaptcha } from 'express-recaptcha'; // Import the express-recaptcha module

import { config } from './utils/config.js';
import { staticFileMiddleware } from './middleware/staticFileMiddleware.js';
import { jsonBodyParser } from './middleware/requestParser.js';
import { SparqlDatabaseClient } from './utils/SparqlDatabase.js';

import path from 'path';

//import { initLanguage } from './controllers/languageController.js';

// Express config
import donateRouter from './routes/donateRouter.js';
import aboutRouter from './routes/aboutRouter.js';
//import languageRouter from './routes/languageRouter.js';

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




// Checks whether the browser accepts one of the languages ('de', 'en'). If not, 'en' is set as the default language. The 'initLanguage' function is then executed.
app.use('/:langId(de|en|ja)?/', (req, res, next) => {
  
  console.log('route parameter gets langId', req.params.langId);

  req.lang = 'en';

  if (req.params.langId) {
    req.lang = req.params.langId;
  } else {
    const lang = req.acceptsLanguages('de', 'ja', 'en');
    //console.log(req.headers['accept-language']);
    console.log('Accepted browser language:', lang);

    if (lang) {
      req.lang = lang;
    } 
  
  }
  console.log('Application language is:', req.lang);
  //initLanguage(lang);
  //res.redirect(301, '/' + req.lang + '/donate');
  next();
});

// Routes
app.get('/:langId(de|en|ja)/', (req, res) => {
    res.redirect(301, '/' + req.lang + '/donate');
});

app.use('/:langId(de|en|ja)/donate', donateRouter);
app.use('/:langId(de|en|ja)/about', aboutRouter);
//app.use('/:langId(de|en|ja)/clang', languageRouter);

app.use( (req, res, next) => {
  if (req.url.startsWith('/' + req.lang + '/')) {
    next();
  } else {
    res.redirect(301, path.join('/', req.lang, req.url));
  }
});

/*app.use(
  middleware.handle(i18next, {
    ignoreRoutes: ["/foo"], // or function(req, res, options, i18next)
    removeLngFromUrl: false
  })
)*/

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
