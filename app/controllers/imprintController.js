import { loadMarkdown } from '../utils/markdown.js';
import { renderLocalizedView } from './defaultController.js';


export function renderImprint(req, res) {
  const html = loadMarkdown(req.lang, 'imprint');
  const data = { ...getLanguageMessages(req.lang), pageHtml: html };
  renderLocalizedView(req, res, 'imprint', data);
}
