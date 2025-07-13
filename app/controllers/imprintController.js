import { loadMarkdown } from '../utils/markdown.js';
import { renderLocalizedView } from './defaultController.js';
import { getLanguageMessages } from '../utils/localization.js';

export async function renderImprint(req, res, next) {
  try {
    const html = await loadMarkdown(req.lang, 'imprint');
    const data = { ...getLanguageMessages(req.lang), pageHtml: html };
    renderLocalizedView(req, res, 'imprint', data);
  } catch (err) {
    console.error('Error rendering imprint:', err);
    next(err); // or res.status(500).send('Error loading page')
  }
}