import bodyParser from 'body-parser';
import express from 'express';
import path from 'path';
import cookieParser from 'cookie-parser';

import { jsonBodyParser } from './middleware/requestParser.js';
import { staticFileMiddleware } from './middleware/staticFileMiddleware.js';
import { config } from './utils/config.js';
import { getLanguageCodes, getLanguageMessages, loadLanguageFiles } from './utils/localization.js';

// Express config
import aboutRouter from './routes/aboutRouter.js';
import demoRouter from './routes/demoRouter.js';
import donateRouter from './routes/donateRouter.js';
import thanksRouter from './routes/thanksRouter.js';
import contactRouter from './routes/contactRouter.js';
import rewardRouter from './routes/rewardRouter.js';
import imprintRouter from './routes/imprintRouter.js';
import privacyRouter from './routes/privacyRouter.js';
import accessibilityRouter from './routes/accessibilityRouter.js';

const app = express();
app.set('view engine', 'ejs');
app.set('views', path.join(path.resolve(), 'views'));
const port = config.port;
const contextPath = process.env.APP_BASE_PATH || '/';
console.log('ContextPath: ', contextPath);

const router = express.Router();

// Enable language functions
loadLanguageFiles();
const validLanguageCodes = getLanguageCodes().join('|');

// Use bodyParser and express-recaptcha module
router.use(bodyParser.urlencoded({ extended: true }));
router.use(bodyParser.json()); // Added to parse JSON bodies

// Middleware for parsing form data in the request body
router.use(jsonBodyParser);

// Middleware for serving static files
router.use(staticFileMiddleware);

app.get('/test-disclaimer', (req, res) => {
  res.send('Disclaimer Test Route Reached ✅');
});


// Either sets req.lang to the already set route language parameter or gets the preferred browser language. Default value is 'en'.
router.use('/:lng(' + validLanguageCodes + ')?/', (req, res, next) => {
  console.log("Disclaimer route middleware hit")
  console.log('Language use: ', req.url);

  //console.log('Route language parameter:', req.params.lng);
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
  res.locals.messages = getLanguageMessages(req.lang);
  console.debug('Application language:', req.lang);
  next();
});

import { requireAgeConsent } from './middleware/ageGateMiddleware.js';
import disclaimerRouter from './routes/disclaimerRouter.js';



// Public routes (no age check)
router.use('/:lng(' + validLanguageCodes + ')/disclaimer', disclaimerRouter);
router.use('/:lng(' + validLanguageCodes + ')/imprint', imprintRouter);
router.use('/:lng(' + validLanguageCodes + ')/privacy', privacyRouter);
router.use(
  '/:lng(' + validLanguageCodes + ')/accessibility',
  accessibilityRouter
);

// Routes
// Redirects all requests to '/donate' if the language parameter (lng) is already set
router.get('/:lng(' + validLanguageCodes + ')?/', (req, res) => {
  console.log('Redirecting to donate');
  console.log(contextPath + req.lang + '/donate');
  res.redirect(301, contextPath + req.lang + '/donate');
});

// Enforce age confirmation for all other routes
router.use(requireAgeConsent);

router.use('/:lng(' + validLanguageCodes + ')/reward', rewardRouter);
router.use('/:lng(' + validLanguageCodes + ')/contact', contactRouter);
router.use('/:lng(' + validLanguageCodes + ')/donate', donateRouter);
router.use('/:lng(' + validLanguageCodes + ')/about', aboutRouter);
router.use('/:lng(' + validLanguageCodes + ')/demo', demoRouter); //Probably needs to be changed like the ones on the top
router.use('/:lng(' + validLanguageCodes + ')/thanks', thanksRouter);




// Intercepts all calls of '/' and checks whether a language (req.lang) is already set. If not, this parameter is set.
router.use((req, res, next) => {
  console.log('Path: ', req.url);
  if (req.url.startsWith('/' + req.lang + '/')) {
    next();
  } else {
    console.log('Redirecting');
    let p = path.join(contextPath, req.lang, req.url);
    console.log('Redirect-Path', p);
    res.redirect(307, path.join(contextPath, req.lang, req.url));
  }
});

app.use(cookieParser());
app.use(contextPath, router);

// Catch-all route for unmatched routes
app.use((req, res) => {
  console.log('❓ Reached unmatched route:', req.originalUrl);
  res.status(404).send('404 - Not Found');
});

app.listen(port, () => {
  console.log(`Server is running on http://app.localhost`);
});
