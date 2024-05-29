//doesnt work need to fix
import bodyParser from 'body-parser';

//Middleware to parse JSON data in the request body
const jsonBodyParser = bodyParser.json();

//Export the middleware
export { jsonBodyParser };
