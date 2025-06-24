import { getLanguageMessages } from '../utils/localization.js';
import { connect, ObjectId } from '../models/survey.js';

export async function renderSurvey(req, res) {
  try {
    const db = await connect();
    db.collection("surveys")
        .find()
        .toArray()
        .then(console.log);

    const survey = await db
        .collection('surveys')
        .findOne({ id: req.params.id });
    if (!survey) {
        return res.status(404).send('Survey not found');
    }

    res.render(
        "survey",
        {
            survey: survey,
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
    await db
        .collection('results')
        .insertOne({
            surveyId: req.params.id,
            data: req.body,
            submittedAt: new Date()
        });
    res.render("/thanks")
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
