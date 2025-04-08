import express from 'express';
import { renderAccessibilityStatement } from '../controllers/accessibilityController.js';

const router = express.Router();

router.get('/', renderAccessibilityStatement);

export default router;
