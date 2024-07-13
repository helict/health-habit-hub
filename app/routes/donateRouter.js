import express from 'express';
import cookieParser from 'cookie-parser';
import { RecaptchaV2 as Recaptcha } from 'express-recaptcha'; // Import the express-recaptcha module
import {
  showDonateForm,
  saveDonateData,
} from '../controllers/donateControllers.js';

const router = express.Router();

// Required for remembering the experiment setting during a browser session
router.use(cookieParser());

// Configure the reCAPTCHA module with your own keys
const recaptcha = new Recaptcha(
  '6Lc_WPEpAAAAAFmAbljvtUq2lX3Iekior1r3qr7l',
  '6Lc_WPEpAAAAAJKIbXTBmYBGKsZeay4ANUykwh7m',
);
router.use(recaptcha.middleware.render);

// Middleware to add reCAPTCHA to the context
router.use((req, res, next) => {
  res.locals.recaptcha = recaptcha.render();
  next();
});

router.get('/', showDonateForm);
router.post('/data', saveDonateData);

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
