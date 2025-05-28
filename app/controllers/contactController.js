import url from 'url';
import { getLanguageMessages } from '../utils/localization.js';

// Funktion zum Rendern der Contact-Seite
export function renderContactPage(req, res) {
  res.render(
    url.fileURLToPath(new URL('../views/contact.ejs', import.meta.url)),
    getLanguageMessages(req.lang)
  );
}
