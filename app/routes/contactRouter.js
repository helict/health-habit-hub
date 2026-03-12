import express from 'express';
import { renderContactPage } from '../controllers/contactController.js';
import { handleContactForm } from '../controllers/contactController.js';

const router = express.Router();

router.get('/', renderContactPage);
router.post('/submit-form', handleContactForm);

export default router;
