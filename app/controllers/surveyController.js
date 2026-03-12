import { getLanguageMessages } from '../utils/localization.js';
import path from 'path';
import { connect } from '../models/survey.js';

export async function renderSurvey(req, res) {
  try {
    const db = await connect();
    const basepath = req.app.get('basepath') || '';

    // get the currently active survey modules from the admin config
    const config = await db.collection('survey_config').findOne({ configId: 'global_main' });
    if (!config) return res.status(404).send('Survey config missing');
    const activeSurveys = (config.activeSurveys || []).map(s => s.toLowerCase().trim());

    // check the database: What has this user already completed?
    const existingResult = await db.collection('results').findOne({ userId: req.userId });
    const alreadyDone = new Set(existingResult?.completedModules || []);

    // calculate the difference: Which active modules are still missing for the user?
    const missingModules = activeSurveys.filter(name => !alreadyDone.has(name));

    // If the difference is empty and there are active surveys, the user is done. Redirect them.
    if (missingModules.length === 0 && activeSurveys.length > 0) {
      return res.redirect(path.posix.join('/', basepath, req.lang, 'thanks'));
    }

    // load only the pages for the missing modules from the master survey (id: "1")
    const surveyDoc = await db.collection('surveys').findOne({ id: "1" });
    const combinedSurvey = { pages: [], ...config.commonSettings };

    // Filter the master survey to include only the pages for the modules the user hasn't completed yet.
    if (surveyDoc && Array.isArray(surveyDoc.pages)) {
      combinedSurvey.pages = surveyDoc.pages.filter(page => {
        const pageName = (page.name || '').toLowerCase().trim();
        return missingModules.includes(pageName);
      });
    }

    res.render("survey", {
      survey: combinedSurvey,
      locale: req.lang,
      ...getLanguageMessages(req.lang)
    });
  } catch (err) {
    console.error("Render Survey Error:", err);
    res.status(500).send('Server error');
  }
}

export async function submitSurvey(req, res) {
  try {
    const db = await connect();
    const basepath = req.app.get('basepath') || '';

    // Which modules were active during this session?
    const config = await db.collection('survey_config').findOne({ configId: 'global_main' });
    if (!config) throw new Error("Survey config missing"); // Safety check to prevent crashes if config is missing
    const currentlyActive = (config.activeSurveys || []).map(s => s.toLowerCase().trim());

    // Load the user's existing entry to merge new data into it.
    const existingEntry = await db.collection('results').findOne({ userId: req.userId });

    // Merge the answers in a structured way.
    // loads the master survey to map questions to their respective modules
    const surveyDoc = await db.collection('surveys').findOne({ id: "1" });
    if (!surveyDoc) throw new Error("Master survey document with id: '1' not found.");

    // Create a quick lookup map from question name to module name.
    const questionToModuleMap = {};
    surveyDoc.pages.forEach(page => {
      const moduleName = (page.name || '').toLowerCase().trim();
      if (moduleName && Array.isArray(page.elements)) {
        page.elements.forEach(question => {
          if (question.name) {
            questionToModuleMap[question.name] = moduleName;
          }
        });
      }
    });

    // Update the list of completed modules.
    // figures out which modules were completed in THIS submission
    const alreadyDone = new Set(existingEntry?.completedModules || []);
    const submittedModules = currentlyActive.filter(name => !alreadyDone.has(name));

    const newAnswersFlat = req.body.data || {};
    const mergedData = existingEntry?.data || {}; // Start with old data

    // Initialize objects for all submitted modules, even if they are empty, to ensure they appear in the data.
    submittedModules.forEach(moduleName => {
      if (!mergedData[moduleName]) {
        mergedData[moduleName] = {};
      }
    });

    for (const questionName in newAnswersFlat) {
      // Check for own properties to avoid iterating over prototype chain.
      if (Object.prototype.hasOwnProperty.call(newAnswersFlat, questionName)) {
        const moduleName = questionToModuleMap[questionName];
        if (moduleName) {
          if (!mergedData[moduleName]) {
            mergedData[moduleName] = {};
          }
          mergedData[moduleName][questionName] = newAnswersFlat[questionName];
        } else {
          console.warn(`Survey question "${questionName}" could not be mapped to a module and was not saved.`);
        }
      }
    }

    const mergedModules = Array.from(new Set([
      ...(existingEntry?.completedModules || []),
      ...submittedModules
    ]));

    // UPSERT: Update the existing document or create a new one if it doesn't exist.
    // We use $set for data that should be updated and $setOnInsert for the creation date.
    await db.collection('results').updateOne(
      { userId: req.userId }, 
      { 
        $set: { 
          data: mergedData,
          completedModules: mergedModules,
          updatedAt: new Date()
        },
        $setOnInsert: { 
          createdAt: new Date(),
        } 
      },
      { upsert: true }
    );

    const normalizedBasepath = basepath.endsWith('/') ? basepath : `${basepath}/`;
    res.redirect(`${normalizedBasepath}${req.lang}/thanks`);
  } catch (err) {
    console.error("Submit Survey Error:", err);
    res.status(500).json({ status: 'error', message: err.message });
  }
}
