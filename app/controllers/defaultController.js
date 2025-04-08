import url from 'url';
import { getLanguageMessages } from '../utils/localization.js';

export function renderLocalizedView(req, res, pageName) {
  // TODO: Missing / wrong parameter handling
  const pageUrl = new URL('../views/' + pageName + '.ejs', import.meta.url);
  const pagePath = url.fileURLToPath(pageUrl);
  res.render(pagePath, getLanguageMessages(req.lang));
}
