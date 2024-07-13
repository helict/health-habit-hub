import express from 'express';
import { renderDemoPage, saveDemoData } from '../controllers/demoController.js';

const router = express.Router();

router.get('/', renderDemoPage);
router.post('/submit', saveDemoData);

export default router;
