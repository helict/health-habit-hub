import express from 'express';
import { renderPrivacyPolicy } from '../controllers/privacyController.js';

const router = express.Router();

router.get('/', renderPrivacyPolicy);

export default router;
