//doesnt work need to fix
const bodyParser = require('body-parser');

//Middleware to parse JSON data in the request body
const jsonBodyParser = bodyParser.json();

//Export the middleware
module.exports = {
  jsonBodyParser,
};
