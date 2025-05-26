import express from 'express';
import { renderRewardPage } from '../controllers/rewardController.js';

const router = express.Router();

router.get('/', renderRewardPage);

export default router;
