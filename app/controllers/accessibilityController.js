import { loadMarkdown } from '../utils/markdown.js';
import { renderLocalizedView } from './defaultController.js';
import { getLanguageMessages } from '../utils/localization.js';

export async function renderAccessibility(req, res, next) {
  try {
    const html = await loadMarkdown(req.lang, 'accessibility');
    const data = { ...getLanguageMessages(req.lang), pageHtml: html };
    renderLocalizedView(req, res, 'accessibility', data);
  } catch (err) {
    console.error('Error rendering accessibility page:', err);
    next(err); // or res.status(500).send('Error loading page')
  }
}