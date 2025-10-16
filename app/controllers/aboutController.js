import url from 'url';
import { getLanguageMessages } from '../utils/localization.js';
import contexts from '../models/contexts.js';

// Funktion zum Rendern der About-Seite
export function renderAboutPage(req, res) {
  res.render(
    url.fileURLToPath(new URL('../views/about.ejs', import.meta.url)),
    {
      ...getLanguageMessages(req.lang),
      contexts
    }
  );
}
