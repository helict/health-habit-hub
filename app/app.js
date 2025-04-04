import bodyParser from 'body-parser';
import express from 'express';
import path from 'path';

import { jsonBodyParser } from './middleware/requestParser.js';
import { staticFileMiddleware } from './middleware/staticFileMiddleware.js';
import { config } from './utils/config.js';
import { getLanguageCodes, loadLanguageFiles } from './utils/localization.js';

// Express config
import aboutRouter from './routes/aboutRouter.js';
import demoRouter from './routes/demoRouter.js';
import donateRouter from './routes/donateRouter.js';
import thanksRouter from './routes/thanksRouter.js';

const app = express();
const port = config.port;

// Enable language functions
loadLanguageFiles();
const validLanguageCodes = getLanguageCodes().join('|');

// Use bodyParser and express-recaptcha module
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json()); // Added to parse JSON bodies

// Middleware for parsing form data in the request body
app.use(jsonBodyParser);

// Middleware for serving static files
app.use(staticFileMiddleware);

// Either sets req.lang to the already set route language parameter or gets the preferred browser language. Default value is 'en'.
app.use('/:lng(' + validLanguageCodes + ')?/', (req, res, next) => {
  console.debug('Route language parameter:', req.params.lng);
  req.lang = 'en';

  if (req.params.lng) {
    req.lang = req.params.lng;
  } else {
    const lang = req.acceptsLanguages(getLanguageCodes());
    console.debug('Accepted browser language:', lang);

    if (lang) {
      req.lang = lang;
    }
  }
  res.locals.currentLanguage = req.lang;
  console.debug('Application language:', req.lang);
  next();
});

// Routes
// Redirects all requests to '/donate' if the language parameter (lng) is already set
app.get('/:lng(' + validLanguageCodes + ')?/', (req, res) => {
  res.redirect(301, '/' + req.lang + '/donate');
});

app.use('/:lng(' + validLanguageCodes + ')/donate', donateRouter);
app.use('/:lng(' + validLanguageCodes + ')/about', aboutRouter);
app.use('/:lng(' + validLanguageCodes + ')/demo', demoRouter); //Probably needs to be changed like the ones on the top
app.use('/:lng(' + validLanguageCodes + ')/thanks', thanksRouter);

// Intercepts all calls of '/' and checks whether a language (req.lang) is already set. If not, this parameter is set.
app.use((req, res, next) => {
  console.debug('UI Language:', req.lang);
  if (req.url.startsWith('/' + req.lang + '/')) {
    next();
  } else {
    res.redirect(307, path.join('/', req.lang, req.url));
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://app.localhost`);
});
