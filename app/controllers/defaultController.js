import url from 'url';
import { getLanguageMessages } from '../utils/localization.js';

export function renderLocalizedView(req, res, pageName, extraData = {}) {
  const messages = getLanguageMessages(req.lang);

  const pageUrl = new URL('../views/${pageName}.ejs', import.meta.url);
  const pagePath = url.fileURLToPath(pageUrl);

  const data = {
    ...messages,
    lang: req.lang,     // explicit language info in template
    ...extraData        // custom variables like pageHtml
  };

  res.render(pagePath, data);
}