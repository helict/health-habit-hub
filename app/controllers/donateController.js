import url from 'url';
import contexts from '../models/contexts.js';
import { ExperimentGroup } from '../models/experimentGroup.js';
import { getLanguageMessages } from '../utils/localization.js';
import { DbClient } from '../utils/SparqlDatabase.js';
import { config } from '../utils/config.js';

function getExperimentGroupFromQuery(req) {
  if (req.query.group) {
    try {
      return ExperimentGroup.fromString(req.query.group);
    } catch {
      console.error(
        `Ignoring invalid experiment group parameter "${req.query.group}".`
      );
      return null;
    }
  }
}

function getExperimentGroupFromCookie(req) {
  console.log(`Request cookie: experimentGroup=${req.cookies.experimentGroup}`);

  if (req.cookies.experimentGroup) {
    try {
      return ExperimentGroup.fromString(req.cookies.experimentGroup);
    } catch {
      console.error(
        `Invalid experiment group cookie parameter "${req.cookies.experimentGroup}".`
      );
      return null;
    }
  } else {
    return null;
  }
}

// If query parameter 'group' is set, use it to determine experiment group.
// Else, if experiment group cookie is set, use matching experiment group.
// Else, select random experiment group and remember choice in session cookie.
function getExperimentGroup(req, res) {
  const experimentGroupFromQuery = getExperimentGroupFromQuery(req);
  if (experimentGroupFromQuery) {
    console.log(
      `Using experiment group from query: ${experimentGroupFromQuery}`
    );
    return experimentGroupFromQuery;
  } else {
    const experimentGroupFromCookie = getExperimentGroupFromCookie(req);
    if (experimentGroupFromCookie) {
      console.log(
        `Using experiment group from cookie: ${experimentGroupFromCookie}`
      );
      return experimentGroupFromCookie;
    } else {
      const randomExperimentGroup = ExperimentGroup.random();
      console.log(
        `Using randomly selected experiment group: ${randomExperimentGroup}`
      );
      res.cookie('experimentGroup', randomExperimentGroup.toString());
      return randomExperimentGroup;
    }
  }
}

export function showDonateForm(req, res) {
  const experimentGroup = getExperimentGroup(req, res);
  res.render(
    url.fileURLToPath(new URL('../views/donate.ejs', import.meta.url)),
    {
      experimentGroup: experimentGroup,
      contexts: contexts,
      locale: req.lang,
      recaptchaSiteKey: config.recaptcha.siteKey,
      ...getLanguageMessages(req.lang),
    }
  );
}

export async function saveDonateData(req, res) {
  const userId = req.userId;  // User-ID direkt aus req holen
  console.log(`Received donate data for user ${userId}:`, req.body);
  // Choose backend for graph storage without affecting surveys/cookies
  let dbClient;
  if (config.graphBackend === 'neo4j') {
    const { Neo4jDbClient } = await import('../utils/Neo4jDatabase.js');
    dbClient = new Neo4jDbClient(config);
  } else {
    dbClient = new DbClient(config);
  }
  const data = {
    ...req.body,
    habitStrength: req.body.habitStrength,
    experimentGroup: ExperimentGroup.fromObject(req.body.experimentGroup),
  };
  console.log("Hier die Daten des Habits die an die DB weitergeleitet werden:")
  console.log(data);

  try {
    await dbClient.insertDonateData(data, userId); 
    const redirectLang = req.body.language || req.lang || 'en';
    const basepath = req.app.get('basepath') || '/';
    const normalizedBasepath = basepath.endsWith('/') ? basepath : `${basepath}/`;

    console.log('Cookies empfangen:', req.cookies);
    console.log(`Prüfe Cookie 'demographicsCompleted': Wert ist "${req.cookies.demographicsCompleted}"`);

    if (req.cookies.demographicsCompleted === 'true') {
      console.log("Entscheidung: Cookie ist gesetzt. Leite weiter zur Dankesseite.");
      res.redirect(`${normalizedBasepath}${redirectLang}/thanks`);
    } else {
      console.log("Entscheidung: Cookie ist NICHT gesetzt oder falsch. Leite weiter zur Umfrage.");
      res.redirect(`${normalizedBasepath}${redirectLang}/survey/1`);
    }
  } catch (error) {
    console.log(data, userId)
    console.error('Fehler beim Speichern der Spendendaten:', error);
    res.status(500).send('Fehler beim Speichern der Daten.');
  }
}
