import url from 'url';
import { getLanguageMessages } from '../utils/localization.js';
import { ALL_EXPERIMENT_GROUPS } from '../models/experimentGroup.js';
import { loadExperimentConfig } from '../configuration/experimentConfig.js';

export async function renderAdminPage(req, res) {
  const cfg = await loadExperimentConfig();

  const groups = ALL_EXPERIMENT_GROUPS.map(g => {
    const id = g.toString();
    return {
      id,
      label: id.replace(/_/g, ' '),
      enabled: Array.isArray(cfg.enabledGroups) && cfg.enabledGroups.includes(id),
    };
  });

  const locals = Object.assign(
    {},
    getLanguageMessages(req.lang),
    { groups, useAll: !!cfg.useAllGroups, baseUrl: req.baseUrl || '/admin' }
  );

  res.render(
    url.fileURLToPath(new URL('../views/admin.ejs', import.meta.url)),
    locals
  );
}