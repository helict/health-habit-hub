import express from 'express';
import path, { dirname } from 'path';
import { fileURLToPath } from 'url';
import { loadLanguageFiles, getLanguageCodes } from '../utils/localization.js';

loadLanguageFiles();
const validLanguageCodes = getLanguageCodes().join('|');

const __dirname = dirname(fileURLToPath(import.meta.url));

// Create a router to define middleware
const staticFileMiddleware = express.Router();

// Serve CSS files with the 'text/css' MIME type
staticFileMiddleware.use(
  '/:lng(' + validLanguageCodes + ')?/css',
  express.static(path.join(__dirname, '..', 'public', 'css'), {
    extensions: ['css'],
  }),
);

staticFileMiddleware.use(
  '/:lng(' + validLanguageCodes + ')?/js',
  express.static(path.join(__dirname, '..', 'public', 'js'), {
    extensions: ['js'],
  }),
);

staticFileMiddleware.use(
  '/utils',
  express.static(path.join(__dirname, '..', 'public', 'utils'), {
    extensions: ['js'],
  }),
);

// Serve language files with the 'application/json' MIME type
staticFileMiddleware.use(
  express.static(path.join(__dirname, '..', 'public'), {
    extensions: ['json'],
  }),
);

export { staticFileMiddleware };
