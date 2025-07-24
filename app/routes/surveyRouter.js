import cookieParser from 'cookie-parser';
import express from 'express';
import { v4 as uuid } from 'uuid';
import { renderSurvey, submitSurvey } from '../controllers/surveyController.js';

const router = express.Router();

router.use(cookieParser());
router.use((req, res, next) => {
  let userId = req.cookies.userId;
  if (!userId) {
    userId = uuid();
    res.cookie('userId', userId, { maxAge: 365 * 24 * 60 * 60 * 1000, httpOnly: true });
  }
  req.userId = userId;
  next();
});

router.get('/:id', renderSurvey);
router.post('/:id/complete', submitSurvey);

export default router;
