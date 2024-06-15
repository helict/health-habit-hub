import express from 'express';
import { setLanguage } from '../controllers/languageController.js';

const router = express.Router();

router.post('/', setLanguage);

export default router;
