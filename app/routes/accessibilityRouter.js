import express from 'express';
import { renderAccessibility } from '../controllers/accessibilityController.js';

const router = express.Router();

router.get('/', renderAccessibility);

export default router;
