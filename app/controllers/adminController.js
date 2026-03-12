import { getLanguageMessages } from '../utils/localization.js';
import { ALL_EXPERIMENT_GROUPS } from '../models/experimentGroup.js';
import { loadExperimentConfig } from '../configuration/experimentConfig.js';
import { connect } from '../models/survey.js';

export async function renderAdminPage(req, res) {
  try {
    const db = await connect();
    
    // experiment-groups
    const cfg = await loadExperimentConfig();
    const groups = ALL_EXPERIMENT_GROUPS.map(g => ({
      id: g.toString(),
      label: g.toString().replace(/_/g, ' '),
      enabled: Array.isArray(cfg.enabledGroups) && cfg.enabledGroups.includes(g.toString()),
    }));

    // survey-modules
    const surveyDoc = await db.collection('surveys').findOne({});
    const surveyCfg = await db.collection('survey_config').findOne({ configId: 'global_main' }) || {};
    const activePages = surveyCfg.activeSurveys || []; // name of active pages

    let surveyModules = [];
    if (surveyDoc && surveyDoc.pages) {
      surveyModules = surveyDoc.pages.map(page => {
        // 'name' of page as ID
        const pageId = page.name || "Unnamed Page"; 
        return {
          id: pageId,
          label: pageId.replace(/_/g, ' '),
          enabled: activePages.includes(pageId)
        };
      });
    }

    res.render("admin", {
      groups,
      surveyModules,
      useAll: !!cfg.useAllGroups,
      baseUrl: req.baseUrl || '/admin',
      ...getLanguageMessages(req.lang)
    });

  } catch (err) {
    console.error("Admin Page Error:", err);
    res.status(500).send("Internal Server Error");
  }
}

// POST-Handler for config-saving
export async function updateSurveyConfig(req, res) {
  try {
    const db = await connect();
    
    let activeSurveys = req.body.activeSurveys || [];
    if (!Array.isArray(activeSurveys)) activeSurveys = [activeSurveys];

    await db.collection('survey_config').updateOne(
      { configId: 'global_main' },
      { 
        $set: { 
          activeSurveys: activeSurveys,
          updatedAt: new Date()
        } 
      },
      { upsert: true }
    );
    
    const target = req.baseUrl || '/admin';
    
    return res.redirect(target);
  } catch (err) {
    console.error("Update Survey Config Error:", err);
    res.status(500).send("Error saving survey configuration");
  }
}