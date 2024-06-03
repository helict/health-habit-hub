import express from 'express';
import { renderAboutPage } from '../controllers/aboutController.js';

const router = express.Router();

router.get('/', renderAboutPage);

export default router;
