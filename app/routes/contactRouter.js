import express from 'express';
import { renderContactPage } from '../controllers/contactController.js';

const router = express.Router();

router.get('/', renderContactPage);

export default router;
