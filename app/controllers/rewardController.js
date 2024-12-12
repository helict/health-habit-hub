import url from 'url';
import { getLanguageMessages } from '../utils/localization.js';

// Funktion zum Rendern der Contact-Seite
export function renderRewardPage(req, res) {
  res.render(
    url.fileURLToPath(new URL('../views/reward.ejs', import.meta.url)),
    getLanguageMessages(req.lang),
  );
}
