import express from 'express';
import { config } from './utils/config.js';
import { staticFileMiddleware } from './middleware/staticFileMiddleware.js';
import { jsonBodyParser } from './middleware/requestParser.js';
import { SparqlClient } from './utils/SparqlDatabase.js';

// Express config
import donateRouter from './routes/donateRouter.js';
import aboutRouter from './routes/aboutRouter.js';

const app = express();
const port = config.port;

// SPARQL client config
const sparqlClient = new SparqlClient();

// Middleware to parse form data in the request body
app.use(jsonBodyParser);

//Middleware to serve static files
app.use(staticFileMiddleware);

// Routes
app.get('/', (req, res) => {
  res.redirect(301, '/donate');
});
app.use('/donate', donateRouter);
app.use('/about', aboutRouter);

/* eslint-disable */

app.listen(port, () => {
  console.log(`Server is running on http://app.localhost`);
});
