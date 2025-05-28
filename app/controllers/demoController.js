import url from 'url';
import { getLanguageMessages } from '../utils/localization.js';

// Funktion zum Rendern der About-Seite
export function renderDemoPage(req, res) {
  res.render(
    url.fileURLToPath(new URL('../views/demo.ejs', import.meta.url)),
    getLanguageMessages(req.lang)
  );
}

export function saveDemoData(req, res) {
  console.log('Received demographics data:', req.body);
  res.cookie('demographicsCompleted', 'true');
  res.redirect('/thanks');
}
