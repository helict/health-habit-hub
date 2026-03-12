// disclaimerRouter.js

import express from 'express';
import {
  renderDisclaimer,
  acceptDisclaimer
} from '../controllers/disclaimerController.js';

const router = express.Router();

// Diagnostic log middleware
router.use((req, res, next) => {
  console.log('✅ Entered disclaimerRouter:', req.method, req.originalUrl);
  next();
});

router.get('/', renderDisclaimer);
router.post('/', acceptDisclaimer);

export default router;