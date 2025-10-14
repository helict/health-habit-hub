import cookieParser from 'cookie-parser';
import express from 'express';
import { RecaptchaV2 as Recaptcha } from 'express-recaptcha'; // Import the express-recaptcha module
import { v4 as uuid } from 'uuid';
import {
  saveDonateData,
  showDonateForm,
} from '../controllers/donateController.js';
import { config } from '../utils/config.js';

const router = express.Router();

// Required for remembering the experiment setting during a browser session
// and for the user ID. It must come before any middleware that uses cookies.
router.use(cookieParser());

// Middleware to ensure a user ID exists for the session.
// This runs for all routes in this router.
router.use((req, res, next) => {
  let userId = req.cookies.userId;
  if (!userId) {
    userId = uuid();
    // Set a cookie that expires in a year. httpOnly for security.
    res.cookie('userId', userId, { maxAge: 365 * 24 * 60 * 60 * 1000, httpOnly: true });
  }
  // Make userId available on the request object for subsequent handlers
  req.userId = userId;
  next();
});

// Configure the reCAPTCHA module with your own keys
console.log('🔑 reCAPTCHA Config:', {
  siteKey: config.recaptcha.siteKey ? `${config.recaptcha.siteKey.substring(0, 10)}...` : 'MISSING',
  secretKey: config.recaptcha.secretKey ? `${config.recaptcha.secretKey.substring(0, 10)}...` : 'MISSING',
  useRecaptchaDomain: config.recaptcha.useRecaptchaDomain,
  siteKeyLength: config.recaptcha.siteKey.length,
  secretKeyLength: config.recaptcha.secretKey.length,
});

const recaptcha = new Recaptcha(
  config.recaptcha.siteKey,
  config.recaptcha.secretKey,
  {
    useRecaptchaDomain: config.recaptcha.useRecaptchaDomain,
  }
);
// Add reCAPTCHA display to the context
router.use(recaptcha.middleware.render, (req, res, next) => {
  res.locals.recaptcha = res.recaptcha;
  next();
});

router.get('/', showDonateForm);

// The controller function `saveDonateData` will now have access to `req.userId`
// thanks to the middleware above. The previous attempt to pass it as a third
// argument was incorrect as the function only accepts (req, res).
router.post(
  '/data',
  (req, res, next) => {
    // Debug: Log what we received
    console.log('📨 Received reCAPTCHA token:', req.body['g-recaptcha-response'] ? 'Present' : 'MISSING');
    next();
  },
  recaptcha.middleware.verify,
  (req, res, next) => {
    if (!req.recaptcha.error) {
      // Success, proceed to save the data.
      console.log('✅ reCAPTCHA verification passed');
      next();
    } else {
      console.error('❌ reCAPTCHA verification failed:', req.recaptcha.error);
      res.status(400).json({
        error: 'Captcha verification failed. Please try again.',
        details: req.recaptcha.error
      });
    }
  },
  saveDonateData
);

// Route for the contact form with reCAPTCHA verification
//Also probably needs to be changed like the ones on top
router.post('/submit-form', recaptcha.middleware.verify, async (req, res) => {
  if (!req.recaptcha.error) {
    try {
      // Replace these with your actual data processing functions
      // await insertDataClosed(); // Example of a function for data processing
      // await insertDataOpen(); // Example of a function for data processing
      console.log(req.body);
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

export default router;
