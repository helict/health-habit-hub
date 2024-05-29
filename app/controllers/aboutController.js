import url from "url";

// Dummy-Inhalte für die Variablen
const dummyContent = {
  title: "Über Uns - HabitHub",
  aboutText: "Standardtext für Über uns",
  step3Text: "Standardtext für Schritt 3",
  currentLanguage: "EN"
  
};

// Funktion zum Rendern der About-Seite
export function renderAboutPage(req, res) {
  res.render(
    url.fileURLToPath(new URL("../views/about.ejs", import.meta.url)),
    dummyContent
  );
}