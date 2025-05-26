import url from 'url';
import { getLanguageMessages } from '../utils/localization.js';

// Funktion zum Rendern der About-Seite
export function renderThanksPage(req, res) {
  res.render(
    url.fileURLToPath(new URL('../views/thanks.ejs', import.meta.url)),
    getLanguageMessages(req.lang),
  );
}
