import url from 'url';

// Dummy-Inhalte für die Variablen
const dummyContent = {
  title: 'Über Uns - HabitHub',
  aboutText: 'Standardtext für Über uns',
  step3Text: 'Standardtext für Schritt 3',
  currentLanguage: 'EN',
  navigation: {
    homePageName: 'Home',
    aboutPageName: 'About',
    contactPageName: 'Contact',
  },
};

// Funktion zum Rendern der About-Seite
export function renderDemoPage(req, res) {
  res.render(
    url.fileURLToPath(new URL('../views/demo.ejs', import.meta.url)),
    dummyContent,
  );
}