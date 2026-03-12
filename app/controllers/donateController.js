import url from 'url';
import path from 'path';
import contexts from '../models/contexts.js';
import { ExperimentGroup } from '../models/experimentGroup.js';
import { getLanguageMessages } from '../utils/localization.js';
import { DbClient } from '../utils/SparqlDatabase.js';
import { config } from '../utils/config.js';
import { loadExperimentConfig } from '../configuration/experimentConfig.js'; // async config loader

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
  return null;
}

function getExperimentGroupFromCookie(req) {
  const cookieVal = req.cookies && req.cookies.experimentGroup;
  console.log(`Request cookie: experimentGroup=${cookieVal}`);

  if (cookieVal) {
    try {
      return ExperimentGroup.fromString(cookieVal);
    } catch {
      console.error(
        `Invalid experiment group cookie parameter "${cookieVal}".`
      );
      return null;
    }
  } else {
    return null;
  }
}

// pick a random group according to the persisted config (async)
async function pickRandomFromConfig() {
  const cfg = await loadExperimentConfig();

  // if useAllGroups, use uniform random across all 4 groups
  if (cfg && cfg.useAllGroups) {
    return ExperimentGroup.random();
  }

  // else, pick from enabledGroups (stored as array of strings)
  const pool = Array.isArray(cfg && cfg.enabledGroups) ? cfg.enabledGroups.slice() : [];
  if (!pool.length) {
    // fallback: no enabled groups -> use uniform random across all groups
    console.warn('No enabled experiment groups found, falling back to uniform random.');
    return ExperimentGroup.random();
  }

  const pick = pool[Math.floor(Math.random() * pool.length)];
  try {
    return ExperimentGroup.fromString(pick);
  } catch (e) {
    console.error(`Invalid group string in config "${pick}", falling back to random`, e);
    return ExperimentGroup.random();
  }
}

// If query parameter 'group' is set, use it.
// Else, if experiment group cookie is set, use matching experiment group.
// Else, select random experiment group (respecting experimentConfig) and remember choice in cookie.
async function getExperimentGroup(req, res) {
  const experimentGroupFromQuery = getExperimentGroupFromQuery(req);
  if (experimentGroupFromQuery) {
    console.log(
      `Using experiment group from query: ${experimentGroupFromQuery}`
    );
    return experimentGroupFromQuery;
  }

  const experimentGroupFromCookie = getExperimentGroupFromCookie(req);
  if (experimentGroupFromCookie) {
    console.log(
      `Using experiment group from cookie: ${experimentGroupFromCookie}`
    );
    return experimentGroupFromCookie;
  }

  const randomExperimentGroup = await pickRandomFromConfig();
  console.log(
    `Using randomly selected experiment group: ${randomExperimentGroup}`
  );

  // set cookie: 30 days, path '/', sameSite lax, readable by JS (httpOnly: false)
  res.cookie('experimentGroup', randomExperimentGroup.toString(), {
    maxAge: 30 * 24 * 60 * 60 * 1000,
    path: '/',
    sameSite: 'lax',
    httpOnly: false,
  });

  return randomExperimentGroup;
}

export async function showDonateForm(req, res) {
  const experimentGroup = await getExperimentGroup(req, res);
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

  // experimentGroup may come as string or as object.
  let experimentGroupObj;
  try {
    if (!req.body.experimentGroup) {
      // no body value -> try cookie, else pick random from config
      if (req.cookies && req.cookies.experimentGroup) {
        experimentGroupObj = ExperimentGroup.fromString(req.cookies.experimentGroup);
      } else {
        experimentGroupObj = await pickRandomFromConfig();
      }
    } else if (typeof req.body.experimentGroup === 'string') {
      experimentGroupObj = ExperimentGroup.fromString(req.body.experimentGroup);
    } else if (typeof req.body.experimentGroup === 'object') {
      // expects { closedTask: boolean, closedDescription: boolean }
      experimentGroupObj = ExperimentGroup.fromObject(req.body.experimentGroup);
    } else {
      experimentGroupObj = await pickRandomFromConfig();
    }
  } catch (e) {
    console.error('Invalid experimentGroup in request — falling back to random', e);
    experimentGroupObj = await pickRandomFromConfig();
  }

  const data = {
    ...req.body,
    habitStrength: req.body.habitStrength,
    experimentGroup: experimentGroupObj,
  };
  console.log("Hier die Daten des Habits die an die DB weitergeleitet werden:");
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
    console.log(data, userId);
    console.error('Fehler beim Speichern der Spendendaten:', error);
    res.status(500).send('Fehler beim Speichern der Daten.');
  }
}
