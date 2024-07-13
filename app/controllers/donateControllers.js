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
        `Ignoring invalid experiment group parameter "${req.query.group}".`,
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
        `Invalid experiment group cookie parameter "${req.cookies.experimentGroup}".`,
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
      `Using experiment group from query: ${experimentGroupFromQuery}`,
    );
    return experimentGroupFromQuery;
  } else {
    const experimentGroupFromCookie = getExperimentGroupFromCookie(req);
    if (experimentGroupFromCookie) {
      console.log(
        `Using experiment group from cookie: ${experimentGroupFromCookie}`,
      );
      return experimentGroupFromCookie;
    } else {
      const randomExperimentGroup = ExperimentGroup.random();
      console.log(
        `Using randomly selected experiment group: ${randomExperimentGroup}`,
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
      ...getLanguageMessages(req.lang),
    },
  );
}

export async function saveDonateData(req, res) {
  console.log('Received donate data:', req.body);
  const dbClient = new DbClient(config);
  await dbClient.insertDonateData(
    ExperimentGroup.fromObject(req.body.experimentGroup),
    req.body,
  );
  res.sendStatus(200);
}
