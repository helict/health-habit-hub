import { getLanguageMessages } from '../utils/localization.js';
import path from 'path';
import { connect, ObjectId } from '../models/survey.js';

export async function renderSurvey(req, res) {
  try {
    const db = await connect();
    const surveyId = req.params.id;
    console.log(`Attempting to find survey with id: "${surveyId}" (Type: ${typeof surveyId})`);

    const survey = await db
        .collection('surveys')
        .findOne({ id: surveyId });
    if (!survey) {
        console.error(`Survey with id "${surveyId}" not found in MongoDB.`);
        return res.status(404).send('Survey not found');
    }

    res.render(
        "survey",
        {
            survey,
            locale: req.lang,
            ...getLanguageMessages(req.lang)
        }
    );
  } catch (err) {
    console.error(err);
    res.status(500).send('Server error');
  }
}

export async function submitSurvey(req, res) {
  try {
    const db = await connect();
      const submission = {
          surveyId: req.params.id,
          data: req.body,
          submittedAt: new Date(),
          userId: req.userId
      };
      await db.collection('results').insertOne(submission);
      console.log("Survey submission with user ID:", submission);
    res.cookie('demographicsCompleted', 'true', {
        maxAge: 365 * 24 * 60 * 60 * 1000,
        httpOnly: true,
        path: '/' 
    });
    const basepath = req.app.get('basepath') || '/';
    const normalizedBasepath = basepath.endsWith('/') ? basepath : `${basepath}/`;
    res.redirect(`${normalizedBasepath}${req.lang}/thanks`);
  } catch (err) {
    res.status(500).json({
        status: 'error',
        message: err.message
    });
  }
}

//const dbConfig = {
//    host: process.env.MONGO_HOST || "localhost",
//    port: process.env.MONGO_PORT || 27017,
//    database: process.env.MONGO_DB,
//    user: process.env.MONGO_USER,
//    password: process.env.MONGO_PASSWORD
//};
//const client = new MongoClient(`mongodb://${dbConfig.user}:${dbConfig.password}@${dbConfig.host}:${dbConfig.port}/`);
//
//export function renderSurveys(req, res) {
//    client.connect()
//        .then(() => {
//            const db = client.db(dbConfig.database);
//            db.collection("surveys").find().toArray()
//                //.then(console.log)
//                .then(results => {
//                    console.log(results);
//                    res.render(
//                        url.fileURLToPath(new URL('../views/surveys.ejs', import.meta.url)),
//                        {
//                            surveyJson: results[0].json,
//                            ...getLanguageMessages(req.lang)
//                        }
//                    );
//                })
//                .catch(console.error);
//                //.finally(client.close());
//        })
//        .catch(console.error)
//
//    //res.render(
//    //    url.fileURLToPath(new URL('../views/surveys.ejs', import.meta.url)),
//    //    {
//    //        ...getLanguageMessages(req.lang)
//    //    }
//    //);
//}
