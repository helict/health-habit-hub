import express from 'express';
import { renderThanksPage } from '../controllers/thanksController.js';

const router = express.Router();

router.get('/', renderThanksPage);

export default router;