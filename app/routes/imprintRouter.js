import express from 'express';
import { renderImprint } from '../controllers/imprintController.js';

const router = express.Router();

router.get('/', renderImprint);

export default router;
