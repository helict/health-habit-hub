import url from 'url';
import { getLanguageMessages } from '../controllers/languageController.js';

// Funktion zum Rendern der About-Seite
export function renderAboutPage(req, res) {
  res.render(
    url.fileURLToPath(new URL('../views/about.ejs', import.meta.url)),
    getLanguageMessages(),
  );
}
