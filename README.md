# Health Habit Hub

[<img src="./app/public/pics/h3-logo.png" width="250"/>](./app/public/pics/h3-logo.png)

## About

Welcome to our web application, designed to empower users to willingly contribute valuable data pertaining to their habits for research purposes. Our platform offers a seamless experience, allowing users to input data through a randomized selection of four different entry types:

- Closed: Predefined tasks and labels guide users to provide structured data
- Open: An empty text field encourages users to share unstructured information without any influence
- Closed-Task, Open data entry: Predefined task to ensure the right data is submitted but no labeling functionality to leave to user some freedom 
- Open-Task, Closed data entry: No Task, just a textfield with the buttons to label the provided data for well sturctured but less influenced data

#### Data Storage

The data is securely stored in a RDF database hosted on an [Apache Jena Fuseki](https://jena.apache.org/documentation/fuseki2/index.html) SPARQL server. This strategic approach not only ensures efficient data management but also paves the way for easier training of machine learning algorithms using the acquired data.

## Installation

1. Install [Docker](https://www.docker.com/) on your local system.
2. Clone the repository.
3. From within the repository root, start the application with:

```
docker compose watch
```

[Compose Watch](https://docs.docker.com/compose/file-watch/) watches the `./app` directory for changes and will automatically rebuild and restart the `app` Docker container.

**Note:** If you are using a [Mac with Apple silicon](https://support.apple.com/116943), you may need to disable Rosetta emulation in Docker to get the `fuseki` service to run properly. 


## Usage

### Location

#### Online
When inside the TU-Dresden Network you can access the website under:
[http://swdev.wiwi.tu-dresden.de:3000](http://swdev.wiwi.tu-dresden.de:3000) 
And the database under: 
[http://swdev.wiwi.tu-dresden.de:3001](http://swdev.wiwi.tu-dresden.de:3001) 


#### Running the app locally
After running ```docker-compose up``` you can access the following sites: 

Open [app.localhost](https://app.localhost) to use the main application \
Open [fuseki.localhost](http://fuseki.localhost) to see/use the database \
Open [proxy.localhost](http://proxy.localhost) to see the dashboard 

### Donate a habit

To donate a habit, go to `/donate`. You will be randomly assigned to one of the four experiment groups mentioned above. For the duration of your browser session, Health Habit Hub will remember to which experiment group you have been assigned and only show you the corresponding version of the habit entry form.

For debugging, you can also manually select an entry mode by adding a query parameter. Doing so will not change to which experiment group you are assigned to.

- `/donate?group=closed_task_closed_desc`
- `/donate?group=closed_task_open_desc`
- `/donate?group=open_task_closed_desc`
- `/donate?group=open_task_open_desc`

## Repository

The repository contains two services:

- `app` – the _Health Habit Hub_ Node.js app.
- `fuseki` – an Apache Jena Fuseki server instance, initialized with example data and the appropriate schema.

## Development

### Overview

![Architecture diagram](docs/assets/Architecture.svg)

### Utility scripts for development

- `npm run format:check` – Check code format with _Prettier_.
- `npm run lint` – Check for code problems with _ESLint_.
- `npm run test:unitTests` – Run unit tests.

To run all of the above in sequence:

- `npm run test`

To fix code problems:

- `npm run format:fix` – Run _Prettier_ to automatically format code.
- `npm run lint:fix` – Run _ESLint_ to fix all automatically fixable problems.
