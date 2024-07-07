import express from 'express';
import { renderDemoPage } from '../controllers/demoController.js';

const router = express.Router();

router.get('/', renderDemoPage);

export default router;