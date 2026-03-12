import { loadMarkdown } from '../utils/markdown.js';
import { renderLocalizedView } from './defaultController.js';
import { getLanguageMessages } from '../utils/localization.js';

export async function renderPrivacyPolicy(req, res, next) {
  try {
    const html = await loadMarkdown(req.lang, 'privacy');
    const data = { ...getLanguageMessages(req.lang), pageHtml: html };
    renderLocalizedView(req, res, 'privacy', data);
  } catch (err) {
    console.error('Error rendering privacy policy:', err);
    next(err); // or res.status(500).send('Error loading page')
  }
}