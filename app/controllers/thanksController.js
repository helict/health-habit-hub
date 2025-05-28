import url from 'url';
import { getLanguageMessages } from '../utils/localization.js';

export function renderThanksPage(req, res) {
  // grab a shallow copy so we don’t mutate the shared object
  const messages = { ...getLanguageMessages(req.lang) };

  // helper to wrap ALL-CAPS words
  const wrapCaps = str =>
    str.replace(/\b([A-Z]{2,})\b/g, '<span class="caps-green">$1</span>');

  // apply to both thanks and slogan if they exist
  ['thanks', 'slogan'].forEach(key => {
    if (typeof messages[key] === 'string') {
      messages[key] = wrapCaps(messages[key]);
    }
  });

  res.render(
    url.fileURLToPath(new URL('../views/thanks.ejs', import.meta.url)),
    messages
  );
}