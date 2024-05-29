import express from 'express';
import path, {dirname} from 'path';
import {fileURLToPath} from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

// Create a router to define middleware
const staticFileMiddleware = express.Router();

// Serve CSS files with the 'text/css' MIME type
staticFileMiddleware.use('/css', 
  express.static(path.join(__dirname, '..', 'public', 'css'), { 'extensions': ['css'] }));

// Serve JS files with the 'text/javascript' MIME type
staticFileMiddleware.use('/js', 
  express.static(path.join(__dirname, '..', 'public', 'js'), { 'extensions': ['js'] }));

// Serve language files with the 'application/json' MIME type
staticFileMiddleware.use(express.static(path.join(__dirname, '..', 'public'), { 'extensions': ['json'] }));

export { staticFileMiddleware};