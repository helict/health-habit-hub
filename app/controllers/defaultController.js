import url from 'url';
import { getLanguageMessages } from '../utils/localization.js';

export function renderLocalizedView(req, res, pageName, extra = {}) {
  const messages = getLanguageMessages(req.lang);

  const pageUrl = new URL(`../views/${pageName}.ejs`, import.meta.url);
  const pagePath = url.fileURLToPath(pageUrl);

  res.render(pagePath, {
    ...messages,
    lang: req.lang,
    ...extra
  });
}