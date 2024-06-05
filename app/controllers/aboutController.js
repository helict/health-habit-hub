import url from 'url';

// Load language JSON File
import data from '../language/messages_de.json' with {type: 'json'};

// Funktion zum Rendern der About-Seite
export function renderAboutPage(req, res) {
  res.render(
    url.fileURLToPath(new URL('../views/about.ejs', import.meta.url)),
    data
  );
}
