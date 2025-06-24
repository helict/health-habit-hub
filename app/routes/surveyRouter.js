import express from 'express';
import { renderSurvey, submitSurvey } from '../controllers/surveyController.js';

const router = express.Router();
router.get('/:id', renderSurvey);
router.post('/:id/complete', submitSurvey);

export default router;
