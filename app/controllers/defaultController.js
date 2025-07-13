import url from 'url';
import { getLanguageMessages } from '../utils/localization.js';

export function renderLocalizedView(req, res, pageName, extraData = {}) {
  const pageUrl = new URL('../views/' + pageName + '.ejs', import.meta.url);
  const pagePath = url.fileURLToPath(pageUrl);

  // Merge language messages + extra page data (e.g., pageHtml)
  const data = {
    ...getLanguageMessages(req.lang),
    ...extraData
  };
  // Render the page with the provided data
  res.render(pagePath, data);
}