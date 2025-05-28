Health Habit Hub – Developer Guide

Project Purpose and Overview

The Health Habit Hub is a web application that allows users to contribute data about their personal health habits for research purposes ￼. The goal is to collect structured and unstructured habit data from volunteers in a way that can later facilitate machine learning analyses ￼. When a user chooses to “donate” a habit data point, the system randomly assigns them to one of four data entry modes (a 2×2 factorial design) ￼:
• Closed: User is given a predefined task and a set of labels, guiding them to provide highly structured data ￼.
• Open: User is simply given an empty text field with no prompt or categories, encouraging an uninfluenced, free-form response ￼.
• Closed Task, Open Entry: A specific task is provided (ensuring the user provides the intended type of data), but no labels are given – the response is entered as free text ￼.
• Open Task, Closed Entry: No particular task prompt is given (the user decides what habit to describe), but the interface provides labeling buttons or categories to structure the description ￼.

Each of these four modes represents a combination of Task Guidance (Closed vs. Open) and Data Entry Method (Closed/structured vs. Open/unstructured), creating a 2×2 experimental setup. This design enables researchers to examine how different levels of guidance and structure affect the data provided by users.

All user-contributed habit data is stored in a back-end RDF datastore (a semantic graph database). Specifically, the project uses an Apache Jena Fuseki SPARQL server to securely store the habit entries as RDF triples ￼. This approach ensures the data is captured in a flexible, machine-readable format and paves the way for easier training of machine learning algorithms on the collected habits ￼. In summary, Health Habit Hub’s purpose is to gather habit information in various formats and store it in a semantic database for future analysis, all while providing a seamless user experience for participants contributing data.

Architecture

Figure: High-level architecture of the Health Habit Hub system. The Node.js backend (“app” container) serves pages to the user’s browser and communicates with the Fuseki RDF datastore (“fuseki” container) via SPARQL queries.

At a high level, Health Habit Hub follows a client–server architecture with a decoupled back-end and database. The web browser (client) interacts with the Node.js back-end server, which in turn communicates with the Fuseki RDF triple store:
• The Node.js application (the “app” service) is built with Express and serves both the user-facing pages and a RESTful interface for form submissions. It renders HTML pages using EJS templates and includes logic to handle the experimental group assignment and data processing.
• The Fuseki server (the “fuseki” service) acts as an RDF database. The Node app sends SPARQL queries (over HTTP) to the Fuseki server to insert new habit data and potentially to query stored data. Fuseki stores the habit entries in a semantic data model defined by an ontology (schema), which was pre-loaded along with some example data during initialization ￼.
• In the development environment, a reverse proxy or networking setup is used so that the services are accessible via convenient hostnames. For example, the app might be reached at app.localhost and the database at fuseki.localhost on the local machine ￼. This is accomplished via Docker Compose configuration (see Setup below). In production deployments, the app can be bound to standard ports or behind an external proxy for public access.

Within the Node.js application, the architecture is further structured by the separation of concerns between routing, view rendering, and data access (SPARQL queries). The use of Docker containers for the app and database enforces a modular architecture: the Node.js service can be scaled or modified independently of the RDF data store, and vice versa. This modular design also makes it easier for new developers to set up the entire system quickly, as all components and their dependencies are defined in code (via Docker configuration).

Tech Stack and Key Dependencies

The Health Habit Hub project leverages a modern web and semantic technology stack:
• Node.js & Express: The back-end is built on Node.js with the Express framework, providing the web server and routing logic. Express handles HTTP requests (serving pages and receiving form submissions) in a lightweight manner.
• EJS Templates: The front-end HTML is generated using EJS (Embedded JavaScript) templates. This allows dynamic content and conditional UI depending on the user’s experimental group and selected language. EJS templates are rendered on the server side into HTML before being sent to the client.
• HTML, CSS, and JavaScript: Standard web technologies are used for the client-facing portion. The project includes custom CSS (and possibly some framework CSS) for styling the pages, and JavaScript on the client side for any interactive behavior (such as form enhancements or dynamic elements). According to the repository’s statistics, CSS constitutes the largest portion of the codebase ￼, indicating significant styling or possibly inclusion of a CSS framework, while the JavaScript and EJS code form the remainder.
• Docker & Docker Compose: Containerization is used for both development and deployment. Docker ensures that the Node app and the Fuseki database run in isolated, reproducible environments. The provided docker-compose.yml defines two services (app and fuseki) that work together ￼. This means developers do not have to install database or server dependencies directly on their machine – Docker handles it. Additionally, Docker Compose’s Watch mode is used for development (auto-reloading the app on code changes) ￼.
• Apache Jena Fuseki (RDF Triple Store): Fuseki is the database server used to persist the habit data. It supports the SPARQL 1.1 protocol for querying and updating RDF data ￼. The project includes a Fuseki setup with a predefined dataset and ontology (schema) loaded, so that the data model for habits is available from the start ￼.
• SPARQL (Query Language): All data interactions with the Fuseki database use SPARQL, the standard query language for RDF. The Node app likely formulates SPARQL UPDATE statements to insert new habit entries, and could use SPARQL SELECT or ASK queries if any data retrieval or checks are needed.
• Internationalization Libraries: The app is internationalized (supports multiple languages), so it uses an i18n library for managing translation strings. Common choices are packages like i18n or i18next in Node – the code uses one of these to load language files and provide translation functions in routes and templates (e.g., providing text in English or German as needed).
• Testing & Linting Tools: The development stack includes Prettier (code formatter) and ESLint (JavaScript linter) to maintain code quality, as well as a testing framework (likely Jest or Mocha) for unit tests. These are run via npm scripts (see Development section) ￼. They ensure consistent code style and help catch errors early.

Other dependencies likely include Express middlewares (for example, to handle sessions or parsing form data), an HTTP client or SPARQL client library to send queries to Fuseki, and possibly express-session for managing user session (to remember the assigned experiment group). All key runtime dependencies are declared in the Node app’s package.json, and Docker will install them during build. As a new developer, it’s useful to skim the package.json to see all libraries in use (Express, EJS, i18n, etc.) and their versions, to get a sense of the tech stack in detail.

Repository Structure and Important Files

Understanding the repository layout will help you navigate the project. The major directories and files include:
• docker-compose.yml: Configuration for Docker Compose that defines how to run the multi-container application. It likely declares two services: app (Node/Express server) and fuseki (Jena Fuseki database) ￼. It also sets up any networking (such as the custom hostnames) and volume mounts (for persisting data or watching code changes) needed.
• app/ directory: Contains the Node.js application code. Notable contents:
• app/package.json – Node package definition with dependencies and scripts.
• app/server.js or app/app.js – Main entry point to start the Express server (naming may vary). This is where the Express app is configured (middleware, routes, view engine, etc.).
• Routes/Controllers: There may be a sub-folder like app/routes/ or similar where route handling code resides. For example, a file for handling the donation form route (e.g., donation.js or integrated in a main file) that contains the logic for assigning groups and processing submissions.
• Views: app/views/ holds EJS template files that define the HTML structure of pages. You will find templates corresponding to different pages or components of the site. For instance, a donate.ejs (or similarly named) template for the habit donation form, possibly partials for header/footer, etc. These templates include placeholders for dynamic content (like the text of the predefined task, or the list of labels, which the back-end fills in).
• Public Assets: app/public/ contains static files served directly to the client. This includes CSS stylesheets, client-side JavaScript, and image assets. For example, the repository’s logo image (h3-logo.png) is stored here ￼. The CSS likely includes a main stylesheet for the site’s look and feel. Any front-end scripts (for UI interactions on the form, etc.) would also reside here.
• Localization Files: If using a framework like i18n, there might be an app/locales/ folder with subfolders or JSON files for each supported language (e.g., en.json and de.json containing translated text strings). These are loaded by the i18n library to provide translated UI text.
• Configuration/Utilities: The app might have config files (for example, an app/config.js for constants like the SPARQL endpoint URL, dataset name, etc.). Also, utility modules could exist (for constructing SPARQL queries, formatting data, etc.).
• Tests: There could be a directory for tests (e.g., app/test/ or app/**tests**/). Unit test files usually have names like _.spec.js or _.test.js. These tests would validate functions like the group assignment logic or SPARQL query builders.
• fuseki/ directory: Contains everything related to the Fuseki RDF server setup. This might include:
• A Fuseki configuration file (e.g., config.ttl or an assembler file) that defines the dataset and loads the ontology/schema.
• The ontology definition (perhaps a .owl or .ttl file) which defines the classes and properties used to model habit data. For example, an ontology might define a class HabitEntry and properties like hasDescription, hasLabel, etc. This schema is loaded into Fuseki so that incoming data conforms to a known structure.
• Example data file that pre-populates the database (as mentioned in the README ￼). This could be a small RDF/Turtle file with a few sample habit entries to illustrate the data format or to test the system.
• A Dockerfile or instructions on how the Fuseki container is built. If the docker-compose uses the official Fuseki image, it might mount the data/config files from this directory. Otherwise, a custom Dockerfile could copy in the schema and data.
• docs/ directory: Documentation resources. Notably, it contains the architecture diagram (Architecture.svg) shown above ￼. If the team maintains additional markdown docs or diagrams, they would be here. (The presence of \_config.yml suggests GitHub Pages documentation might be configured, but currently the main information is in the README and this guide.)
• Other files: Standard files like .gitignore, .eslintrc or Prettier config (if any custom rules) would be at the root. There might also be an .env.example if environment variables are used to configure things like database endpoints or credentials – however, since this is containerized, configuration is likely handled in docker-compose.yml rather than manual .env files.

As a new developer, start by exploring the app/ directory – check the entry point and the route handling for /donate to see how the app works. Also examine the fuseki/ config to understand the data model. This will give you a clear picture of how everything is organized.

Setup and Development Environment

Setting up Health Habit Hub for development is straightforward thanks to Docker. The project maintainers recommend using Docker Compose to run both the app and database together for a consistent environment. Here’s how to get started: 1. Install Docker: Make sure Docker Engine and Docker Compose are installed on your system ￼. Docker is required since the entire app (and database) runs in containers. You can get Docker Desktop from the official site ￼, which includes Compose. 2. Clone the Repository: Fetch the code from GitHub to your local machine (e.g., via git clone). This will create a health-habit-hub directory with all the files. 3. Start the Application with Docker Compose: In the repository root, run the command:

docker compose up --watch

This uses Docker Compose to build and start both containers, and the --watch (or compose watch) flag enables live-reloading for development ￼. The first time you run this, Docker will download the base images (for Node and Fuseki) and set up the environment. Once up and running, Compose will monitor the ./app directory for any code changes and automatically rebuild/restart the Node app container on the fly ￼. This means you can edit the code and see changes without manually restarting. (If your version of Docker Compose does not support --watch, you can achieve a similar effect with manual restarts or alternative file-watching setups, but Compose Watch is the recommended approach here.)
Note for Apple Silicon Mac users: If you are on an M1/M2 Mac, you may need to adjust Docker settings to ensure the Fuseki container works. Specifically, disable Rosetta 2 emulation for Docker, as the Fuseki service may not run properly under emulation ￼. This is due to Fuseki’s base image compatibility; running it natively (arm64 image) is advised.

    4.	Access the Services: Once docker compose up is running, the app and database will be available on specific addresses:
    •	Health Habit Hub Web App: Visit http://localhost:3000/ in your browser. The app uses URL paths prefixed by language (e.g., /en or /de), so you might go to http://localhost:3000/en/donate for the English donation form ￼. If you are using Docker’s special DNS names, you can also use the address app.localhost in a browser (mapped to the app container’s port) ￼.
    •	Fuseki SPARQL Endpoint and UI: The Fuseki server’s web interface is accessible at http://localhost:3001/ by default (or via fuseki.localhost if configured) ￼. Fuseki provides a web GUI where you can run SPARQL queries and updates on the dataset and view the RDF data. This is useful for debugging – for example, to verify that a donated habit was saved, you can query the dataset here.
    •	Proxy/Dashboard: In the dev setup, proxy.localhost (or a similar address) is mentioned ￼. This likely refers to a development proxy or Traefik dashboard. If a reverse proxy container is configured, it might route these friendly URLs to the right service and provide a dashboard. Opening proxy.localhost in a browser might show a status page listing the running services. (If you’re not on macOS or the DNS names aren’t working, you can rely on the localhost:port addresses as noted above.)

Docker Compose will keep running in your terminal. You should see logs from both the app and fuseki services. If everything started correctly, the Node app log will indicate it’s listening on port 3000, and Fuseki will log that it started and loaded the dataset. 5. Develop Iteratively: As you edit code in the app/ directory, the Compose Watch will detect changes and restart the Node app container. You can then refresh the browser to see your changes. For database or ontology changes, you might have to restart the Fuseki service (since it loads data at startup). You can do that by stopping the compose process (Ctrl+C) and running docker compose up again.

If you prefer to run the Node app directly (outside Docker) for debugging, you can – but you’ll need a running Fuseki server or adjust config to point to a remote Fuseki. In most cases, using Docker for both is simplest, but advanced users can run npm install in app/ and npm start the app locally, with environment variables to connect to the Fuseki container or a local Fuseki instance. Ensure you have Node.js (the version specified in the repo, if any) if you attempt this route.

Finally, when you’re done, you can shut down the dev environment with docker compose down. This will stop and remove the containers. The Fuseki data (if configured with a volume) might persist between runs; if it’s just in memory or not volume-mounted, it will reset each time.

Experimental Design: 2×2 Factorial Group Assignment

One of the unique aspects of this project is the built-in experiment that randomly assigns each user session to one of four groups (corresponding to the 2×2 combinations of task guidance and data entry format). Here’s how it works in practice:

When a user navigates to the “Donate a habit” page (the main form to submit a habit entry), the back-end will randomly assign the user to one of the four experiment groups ￼. This assignment is typically done if the user has not been assigned already in their current session. The assignment is stored (often in the user’s session data or a cookie) so that it persists for that browser session ￼. This way, if the user returns to the donate page or navigates the site, they will continue to see the same version of the form – ensuring consistency for that participant.
• Random Assignment: On the first visit to /donate, the server picks one of the four modes with equal probability. This could be implemented with a simple random number or by cycling through to balance groups. The result is that roughly 25% of users get each variant.
• Session Persistence: Once assigned, the server remembers the user’s group. Likely, the Express app uses sessions (via a cookie) to store something like session.group = "closed_task_open_desc" (for example). As long as the session is active, the app will recognize the user’s group on subsequent requests. This ensures the user cannot inadvertently bounce between experiment conditions – an important detail for experimental control ￼.
• Form Variation: Depending on the assigned group, the rendered form will differ. For example, if the group is Closed Task / Closed Entry, the page will include a specific prompt (task) and a set of categorical labels for the user to choose from. If the group is Open Task / Open Entry, the page will be a single open text box with minimal guidance. All this logic is handled server-side when composing the EJS template (or by choosing different templates). Essentially, the server either passes the group information into the template and uses conditional statements in EJS to show/hide parts of the form, or it routes to distinct templates for each group. Either way, the user sees the variant corresponding to their group.

For debugging or development, the application provides a convenient way to manually override the group assignment via query parameters ￼. By appending ?group=<group_name> to the donate URL, you can force the interface to a particular mode. The available group query values are:
• closed_task_closed_desc – (Closed Task, Closed Description)
• closed_task_open_desc – (Closed Task, Open Description)
• open_task_closed_desc – (Open Task, Closed Description)
• open_task_open_desc – (Open Task, Open Description)

For example, visiting /donate?group=open_task_open_desc will show the fully open version of the form regardless of your assigned group ￼. This is useful for previewing all variants without needing multiple sessions. (Internally, the app likely does not change your official session assignment when you use this parameter – it just overrides the rendering for that request ￼. So your underlying group remains the same unless you start a new session.)

This experimental design is fundamental to the project’s research aims. As a developer, be mindful that any changes to the form or submission process should preserve the distinctions between these four conditions. For example, if you add a new question or feature, consider whether it should appear in all versions or only in some (and implement the logic accordingly).

Backend Logic and SPARQL Integration

The backend of Health Habit Hub is a Node.js Express application that coordinates everything between the user interface and the database. Let’s break down key aspects of the backend logic:

Express Routing and Session Management

The Express app likely defines routes for the main actions of the site. The core route is the donation route (e.g., GET /:lang(d e|en)/donate or simply /donate with language handling). Here’s what happens in this route: 1. Language Handling: The site supports internationalization, so the route may include a language code (for instance, /en/donate for English, /de/donate for German). The Express app might use middleware to detect the :lang parameter and set the locale for the response (so that the correct language strings are used in the template). Alternatively, language might be determined by subdomain or cookie, but the URL approach is straightforward and is shown in usage examples ￼. 2. Experiment Group Assignment: When a request hits the donate route, the handler checks if the user already has a group in their session. If not, it randomly assigns one. This could be as simple as selecting a string from the four options and storing it in req.session.group. Express-session middleware would need to be configured to enable this (likely done at app startup with something like an in-memory store since this is a research app, or possibly using a cookie-based approach). From this point on, req.session.group determines what the user sees. If the route sees a group query parameter (as described above for debugging), it might bypass the random assignment for that request or temporarily set a different value (without persisting it). 3. Rendering the Form: The route then renders an EJS template for the donation form. It will pass the group information to the template (e.g., res.render('donate', { group: req.session.group })). The template uses this to conditionally include the appropriate fields and text. For instance, the template might have logic like:

<% if (group === "closed_task_closed_desc") { %>
<!-- HTML for closed task prompt and closed (categorical) input fields -->
<% } %>

and similarly for other cases. Alternatively, there could be separate templates or partials for each mode, and the server chooses which one to render. But a single template with conditions is easier to maintain and ensures any common elements stay in sync.

    4.	Form Submission Handling: The donation form (in the EJS template) will have an action, likely posting to a route like POST /donate (or /en/donate to stay language-scoped). The backend defines a corresponding POST route to handle form submissions. In this handler, the code will extract the submitted data from req.body. Depending on the group, the expected form fields differ:
    •	In modes with open text entry, there will be a free-text description field.
    •	In modes with closed entry (labels), there might be one or more fields indicating the chosen label(s) or categories (e.g., checkboxes or a select dropdown). In those modes, the user might also still input a description (in the open-task/closed-entry scenario, they’d have a text box plus labels; in closed-task/closed-entry, maybe the description is fixed or minimal and mostly labels).
    •	In closed-task scenarios, the task prompt itself is predefined by the system, so it’s not a user input, but the system knows which task was shown (if there are multiple possible tasks, the one shown might be recorded too).
    5.	SPARQL Update Construction: Once the POST handler has the data, it needs to store it in the RDF database. The backend will construct a SPARQL INSERT query (or an HTTP request payload) to send to Fuseki. For example, it might formulate something like:

PREFIX ex: <http://example.com/habit#>
INSERT DATA {
ex:entry12345 a ex:HabitEntry;
ex:description "User entered text here"@en;
ex:hasLabel ex:Sleep;
ex:group "open_task_closed_desc";
ex:timestamp "2025-05-24T16:25:00Z"^^xsd:dateTime .
}

This is a conceptual example – the actual ontology and predicates (and URIs) will depend on the schema. The key point is that the server translates the form inputs into RDF triples. It likely uses some mapping or straightforward string templating to create the SPARQL command. The group might also be stored with each entry (so researchers know under which condition the data was collected). The backend might generate a unique identifier (URI) for each new habit entry resource (here ex:entry12345) – Fuseki doesn’t auto-generate IDs, so the app must do it (or use an blank node, though identifiable URI is better for future reference).

    6.	Sending to Fuseki: The Node app then sends the SPARQL query to the Fuseki server. This is done via HTTP – typically an HTTP POST to Fuseki’s update endpoint (which by default would be at something like http://fuseki:3030/dataset/update inside the Docker network, or mapped to localhost:3001/dataset/update). There are a few ways the Node code could do this:
    •	Using a simple HTTP library like Node’s built-in https/http module or fetch (since Node 18+ has a fetch API, or using node-fetch).
    •	Using a dedicated SPARQL client library for Node.js that wraps the HTTP calls. (The project might have a dependency for this, but it could be done with basic HTTP post as well.)

The app will likely send the query and then await a response to ensure it succeeded. If Fuseki returns an error (e.g., a syntax error in SPARQL or a violation of ontology constraints), the app should handle that (perhaps logging it or returning an error message). For successful inserts, Fuseki usually returns a success 200 status with no content. 7. Post-submission Response: After storing the data, the backend might redirect the user to a confirmation page or simply render a message like “Thank you for donating your habit!”. Currently, the app may just redisplay the form or show a simplified confirmation, since the focus is data collection. Check the code to see if there’s a res.redirect or similar after insert. If no explicit confirmation page is made, one might consider implementing it for clarity (so users know their submission was received).

In addition to the donation flow, the backend may have other routes:
• A home page or landing page (/ or /index) that explains the project.
• Possibly an about page or FAQ.
• Perhaps health-check endpoints or admin endpoints (though not likely in this context).
• If authentication were needed (it’s not for this public data donation use-case), there would be routes for login, etc., but we assume all participation is anonymous and open.

The backend is also responsible for serving the static files (Express will be configured to serve app/public directory). That means any requests for CSS, images, or client JS are handled by Express static middleware.

SPARQL Query Integration Details

The integration with the SPARQL database (Fuseki) is a critical part of the backend. Fuseki hosts an RDF dataset that the app interacts with. The dataset name might be something generic like “dataset” or a custom name configured in the Fuseki container. From the README we know the Fuseki service is initialized with a schema and example data ￼. This implies:
• The ontology (schema) is present so we know what vocabulary to use in triples.
• Example data gives a reference for how actual data will be stored (you can consult it via the Fuseki UI to see the structure).

When the Node app sends queries:
• Inserts: Use SPARQL Update (INSERT DATA). The app likely accumulates the user input into triples. For example, if a user provided a description “I walked 5,000 steps” and selected label “Exercise”, the app might insert a triple like <entryX ex:description "I walked 5,000 steps"> and <entryX ex:hasCategory ex:Exercise> (assuming ex:Exercise is an individual in the ontology’s category scheme). It might also link the entry to a task if applicable, or just implicitly know by group.
• Selects (if any): The app might not need to retrieve data during normal operation (it’s mostly one-way data collection). However, possibly there could be an admin view or the ability to show the user something after submission (e.g., “so far X habits have been donated”). If present, such features would use SPARQL SELECT queries to get data from Fuseki. For instance, counting triples or retrieving the latest entry. As a developer, you can use the Fuseki UI to run custom queries for debugging or analysis.

The Node app likely keeps the Fuseki endpoint URL configurable. In the Docker environment, it could use the Docker service name (e.g., http://fuseki:3030/ds if fuseki is the container and ds is dataset). In code, you might see this URL constructed or stored in a config. Pay attention to environment variables or config at the top of the app code that specify hostnames or ports for Fuseki.

Error handling: If the Fuseki server is down or the query fails, the app should handle it gracefully. Perhaps it returns a 500 error page. During development, if you encounter issues saving data:
• Check the Docker Compose logs. The Fuseki container log will show if it received the query and if any errors occurred (syntax errors or other issues will be printed there).
• Verify the app is indeed sending the query (you can add console.log in the code around the SPARQL submission to debug).
• Ensure the data respects the ontology (for example, if the ontology expects a certain URI or literal type and the app sends something else, Fuseki might still store it since it’s schema-flexible, but semantic consistency is something to watch for).

In summary, the backend’s role is to mediate between the user and the RDF store: routing and rendering the correct form variant, then translating the submitted form to RDF and using SPARQL to persist it. Understanding this flow will allow you to extend or modify the backend with confidence (for example, adding new fields, adjusting the data model, or implementing additional routes).

Frontend Structure (EJS Templates, Client JS, Styling)

The front-end of Health Habit Hub is relatively lightweight since most logic is server-side. It primarily consists of the rendered HTML pages (via EJS templates) along with static resources (CSS and a bit of client-side JavaScript) to enhance user experience. Here’s what to know:

EJS Templates and Views

All user-facing pages are generated by EJS templates on the server. EJS allows embedding JavaScript code within HTML, which is perfect for injecting dynamic content. The key template(s) in this project include:
• Donation Form Template: This is the main form where users input their habit data. The template is designed to show different content based on the experiment group. For example, in the template, there may be conditional sections like: show a specific instruction text if group is a closed-task type, or show a category selection dropdown if group involves closed data entry. The template likely uses if/else or switch logic on the group variable passed from the backend. Additionally, the template will include labels and placeholders that are internationalized (e.g., it won’t hardcode English text like “Enter your habit” but will use a translation key that is rendered in the correct language).
Example: If using the i18n library, the template might have <label><%= \_\_("habit_form.label.prompt") %></label> for a field label, which will output the correct language string provided in translation files.
• Layout/Partial Templates: Often, projects using EJS have a main layout (containing header, footer, common scripts) and use partials or include mechanism for repeating parts (like a navbar or a language switcher). Check if there is a views/partials or similar directory. For instance, there could be a partial for the page header that includes the project logo and title, maybe language selection links (English/German). These partials are included in pages to avoid duplication.
The layout might include the inclusion of CSS and JS assets (for example, linking the main CSS file and any client-side script). EJS can help here by allowing variables for static path if needed.
• Other Pages: Possibly, a homepage template introducing the project, and maybe a thank-you page after submission. If an error occurs, an error template might be used (Express’s default error handler can render an error page). Given issues in the repository mention a 404 page bug, there might be a custom 404 page template that was intended to be shown for unknown routes.

Tip: To find where in the templates something is defined (like text that appears on screen), search the repository for that text. If it’s a static text, it might be in a translation JSON; if it’s a label, it might be directly in the EJS file or in the locale files. This can guide you to the right template file to edit.

Client-Side JavaScript

The project doesn’t appear to be heavy on front-end scripting (it’s not a single-page app or highly dynamic UI). However, there may be a small amount of JavaScript on the client for things like form validation or interactivity. Potential client-side functionalities:
• Form validation or enhancements: e.g., ensuring required fields are filled, or enabling/disabling a text input based on a selection. (For instance, if a user chooses a label “Other”, perhaps a hidden text field appears to specify what “Other” is – such logic would be client-side.)
• Dynamic elements: If in closed-entry modes the user can select multiple labels or click buttons to tag the entry, a script might handle toggling those or counting them.
• UI/UX improvements: maybe a character counter for the text field, or a confirmation dialog.

All client JS files would be in the app/public directory, perhaps under public/js/. They would be linked in the EJS template (e.g., <script src="/js/main.js"></script> in the layout). If no custom JS file exists, it means the site might rely purely on HTML forms and basic behavior (which is possible for a simple form).

As a new dev, open the donate page in your browser’s developer tools and see if any script files are loaded. That will tell you what front-end JS exists. You can then read those files to understand their behavior.

CSS and Styling

Health Habit Hub includes a significant amount of CSS (over 80% of the codebase by lines ￼). This suggests a comprehensive custom style or maybe included CSS frameworks:
• It could be a custom stylesheet (style.css) that defines the look (colors, layout, responsiveness).
• Alternatively, a CSS framework like Bootstrap or Bulma might have been included. If so, their CSS files are large and would explain the high CSS percentage. Check public/css/ for clues (file names like bootstrap.min.css or similar). If a framework is used, you’ll want to be familiar with its classes when editing the front-end.

Regardless, the styling defines how the form looks – including layout of the label buttons, the text field, etc. The pink H3 logo (visible in the repository) suggests a color scheme (pink/white/grey perhaps) that might be used throughout for branding.

If you plan to modify the UI, understanding the CSS structure is important. Follow any naming conventions in the CSS (for example, CSS classes might be prefixed or structured in a certain way). If a framework is used, leverage its grid or utility classes rather than reinventing the wheel, for consistency.

For responsive design: ensure that any new elements you add are mobile-friendly. If using a framework, stick to its responsive grid. If custom CSS, test the pages on different screen sizes (using dev tools) to confirm the form is usable on mobile devices.

Internationalization on the Frontend

While internationalization involves backend loading of strings, it directly affects the front-end because all visible text should come from translations. Pay attention to how the templates get those strings:
• Possibly, an \_\_() or similar function is available in EJS templates to output the right language text.
• The language is determined by the URL or session as noted, so ensure when adding new text in templates, you add corresponding keys to both English and German resource files.

Example: If you add a new field with label “Motivation”, do not hardcode “Motivation:” in the template. Instead, add an entry in en.json like "motivation_label": "What is your motivation?" and in de.json the German equivalent, then use \_\_("motivation_label") in the EJS. This way, the app remains fully translatable.

One of the reported issues was “Translation Services” bug – which implies maybe some text didn’t translate or the mechanism wasn’t working. Keep an eye out for any template content that might not be properly wrapped in translation calls. Fixing those would be valuable (for instance, maybe the placeholders or validation messages need to be translated).

Static Pages and Assets

If the project includes any static informational pages (like an ethics disclaimer or a privacy policy), those might just be simple EJS templates without much dynamic content. Styling and translation considerations still apply.

The images (like the logo) are served from the public folder. Use them as needed in the templates (e.g., <img src="/pics/h3-logo.png" alt="Health Habit Hub Logo">). Additional images can be added to illustrate things if necessary (just drop them in public/pics and reference accordingly).

In summary, the front-end is a conventional server-rendered interface:
• Edit EJS templates for structural and textual changes (remembering to use i18n keys for text).
• Edit/add CSS for style changes (keeping style consistent across all experiment modes).
• Add client JS if needed for enhanced interactions (but avoid overly complex scripts; keep it simple and tested in all modes).

By keeping front-end changes minimal and clear, we ensure that all four versions of the form remain user-friendly and consistent.

RDF Data Model and Ontology Usage

Health Habit Hub uses a semantic data model to store habit information. This means instead of relational tables, data is stored as triples (subject–predicate–object) in an RDF graph. An ontology (or schema) defines the structure of this data – essentially, it specifies what types of entities and properties exist for the habit data. Understanding the ontology will help you know how to record or query information.

Ontology Structure

Upon setup, the Fuseki service is initialized with the appropriate schema for the project ￼. While the documentation does not list the exact ontology, we can infer a plausible model:
• There is likely a class representing a Habit Entry (for example, HabitEntry or HabitRecord). Each time a user donates a habit, an instance of this class is created.
• Properties of a Habit Entry might include:
• Description/Text: The free-text provided by the user about their habit. This could be a property like hasDescription or something from a standard vocabulary (perhaps using rdfs:comment or Dublin Core’s description, but a custom property is fine). The value of this property is a string literal, possibly with a language tag (e.g., "walked 5000 steps"@en).
• Category/Label: If the entry mode involved structured labels, those labels would be recorded. The ontology might define a controlled vocabulary for habit categories (e.g., Exercise, Diet, Sleep, etc.). Possibly a class HabitCategory with individuals like Exercise, Nutrition, etc., and the Habit Entry has a property like hasCategory linking to one of those. In modes where users didn’t pick a label, this property might simply be absent.
• Task Prompt: For closed-task modes, the specific task given might be worth recording (especially if multiple tasks exist). The ontology could have individuals for tasks or a property wasPromptedWith linking the entry to a Task entity (or simply a literal describing the task). If there’s only one predefined task, this might not be stored per entry since it’s constant; but if tasks vary, capturing which one the user got is useful.
• Timestamp: It’s often useful to timestamp entries (when submitted). There could be a property like dc:created or a custom submissionTime with an xsd:dateTime value. This wasn’t mentioned explicitly, but in research data it’s common to store.
• Group/Condition: The experimental condition could also be stored as a data property or an annotation on the entry (e.g., hasEntryMode "open_task_closed_desc"). This is not strictly needed if you can infer it from context (like if certain properties being present/absent indicate the mode), but explicitly storing the group makes analysis easier later. The example schema may have that, or it could be left for external analysis.
• Additionally, the ontology might reuse some well-known vocabularies where appropriate. For example, if recording a user or participant (though here likely not, since it’s anonymous), one could use FOAF or schema.org’s Person – but I suspect each entry is standalone without personal info. Or for categories, they might link to external vocabularies (perhaps not; a self-contained approach is fine).

The ontology could be defined in a Turtle or OWL file in the repository. Loading that into a tool like Protégé could give a clear picture. If you locate the file (maybe in fuseki/ontology.ttl), it will list classes (owl:Class) and properties (owl:ObjectProperty or owl:DatatypeProperty). Keep those in mind when writing SPARQL or modifying data.

Storing Data in RDF (Example)

To illustrate, imagine a user donated a habit with the following scenario:
• Group: Open Task, Closed Entry (so no predefined task, but they selected a label/category).
• They wrote “Drank 8 glasses of water” as the description.
• They selected the category “Hydration” (just a hypothetical label in the ontology).

The triples stored might be (in Turtle syntax):

:entry_abc123 rdf:type :HabitEntry ;
:hasDescription "Drank 8 glasses of water"@en ;
:hasCategory :Hydration ;
:entryMode "open_task_closed_desc" ;
:submittedAt "2025-05-24T18:25:00+02:00"^^xsd:dateTime .

Here :entry_abc123 is a new resource (subject) for this entry. It’s of type HabitEntry. It has a description literal with language tag English. It hasCategory pointing to :Hydration (which would be defined elsewhere as a HabitCategory). We also store the mode as a literal and a timestamp. The prefixes (like :) represent some base URI defined by the ontology (often projects use something like http://yourdomain/health-habits# as a base for their terms).

Querying Data

As a developer, you might need to query the RDF data for debugging or extension tasks:
• Viewing all entries: A SPARQL SELECT could retrieve all ?entry where ?entry rdf:type :HabitEntry to list all entries and maybe their descriptions or categories. This could be done in the Fuseki web UI.
• Filtering by category or content: You could query for all habit entries that have a certain category, or do a text search if Fuseki is configured for full-text (likely not out-of-the-box, but you can filter by literal content with regex if needed).
• Counting entries per mode: If mode is stored as a property, a query grouping by mode can tell how many entries were collected in each experimental condition, which might be a quick check for balanced data.
• Checking for data integrity: For example, ensure every HabitEntry has either a category or not depending on mode, etc.

Ontology and Data Updates

If you need to extend the ontology (for instance, to add a new property or category):
• Modify the ontology file in fuseki/ (e.g., add a new owl:DatatypeProperty :hasMotivationText if we want to store a new survey question answer like “Why do you do this habit?”). Keep consistent naming and define domains/ranges if needed for clarity (though Fuseki doesn’t enforce them strictly, it’s good documentation).
• You would then have to reload the Fuseki data with the new ontology. In dev, it might mean restarting the Fuseki container. Ensure the Docker config picks up changes (the ontology might be loaded from a persistent volume or on each start). If it’s only loaded on container init, you might need to rebuild or volume-mount the updated file.

When inserting data that touches a new ontology element (like a new property), make sure the SPARQL uses the correct prefixes and that the Fuseki dataset knows about that prefix. Often the ontology file will define a prefix (like @prefix ex: <http://.../habit#>) which you should use. In SPARQL, you might have to add a PREFIX declaration at top of your query for any new prefixes.

Given the RDF nature, the system is flexible – you can add triples with new properties even if the ontology wasn’t updated, and the triple store will accept them (RDF is schemaless in enforcement). However, for the data to be semantically coherent and for others to understand it, update the ontology accordingly and document the changes.

One more thing: the Fuseki UI (YASGUI) allows you to set default prefixes for easier querying. The team might have configured common prefixes (like rdf, rdfs, xsd) and their own ontology prefix in the Fuseki UI. This makes writing queries more convenient (you can refer to classes/properties with a short prefix instead of full URIs).

Internationalization (i18n) Support

Health Habit Hub is designed to be bilingual (at minimum English and German, given the context). Internationalization (i18n) is implemented to allow the interface text to appear in multiple languages without duplicating templates. Here’s how i18n is integrated and how to work with it:
• Language Detection: The application likely determines the user’s language either from the URL path (e.g., /en/ vs /de/) or possibly from browser settings. The README examples clearly show /en/donate and mention being inside the TU Dresden network (which implies German might be the other language) ￼. It’s common to include the locale in the route; if so, the Express app probably has routes prefixed with /:lang. If the user hits the root or an undefined locale, it might default to English or redirect to a default.
• Language Files: For managing translations, the project uses a mechanism (likely a library) where all translatable strings are stored in resource files. Typically, we’d expect something like locales/en.json and locales/de.json (or .js files, or YAML, depending on the library). Each file contains key-value pairs mapping message keys to the actual text in that language. For example:

// en.json
{
"app_title": "Health Habit Hub",
"donate_prompt": "Donate a Habit",
"label_exercise": "Exercise",
"label_diet": "Diet",
...
}

// de.json
{
"app_title": "Health Habit Hub",
"donate_prompt": "Spende eine Gewohnheit",
"label_exercise": "Bewegung",
"label_diet": "Ernährung",
...
}

The actual keys and structure will match the text used in templates. The library will load these files based on the current locale and provide a function to fetch the string.

    •	i18n Library (Express integration): A commonly used library is i18n for Express, which adds a __ function to the res object or globally. Another is i18next with middleware. If the code uses i18n, you might see an initialization like:

const i18n = require('i18n');
i18n.configure({
locales: ['en', 'de'],
directory: \_\_dirname + '/locales'
});
app.use(i18n.init);

This would auto-detect locale from req or allow manual setting. If using i18next, the setup is similar but a bit more involved (with middleware to attach req.t function, etc.).

    •	Using Translations in Templates: In EJS, after i18n is configured, you can use the provided functions to insert text. For example, with i18n library, <%= __('donate_prompt') %> would output “Donate a Habit” or its German equivalent based on the current locale. If using i18next, it might be <%= t('donate_prompt') %> depending on how it’s exposed. The issues list had a title “Translation Services” which might mean there was a bug in how translations were rendered (perhaps a missing function in templates). If you see something like <%= t('key') %> not outputting, ensure the template has access to t (with i18next, the middleware must attach it to res.locals or similar).
    •	Switching Languages: How can a user switch language? If the URL path approach is used, simply visiting the /de/... path shows German. There might be links or a toggle in the UI that points to the other language. For example, a German flag icon linking to the equivalent /de/donate when on /en/donate, and vice versa. If it’s not implemented, a user could manually change the URL. For development, test both language URLs to see that all text appears translated (you may notice some strings not translated – those would need fixing by adding to the locale files).
    •	Adding/Modifying Translations: If you need to change wording, update the corresponding entry in the language files. Keep the English and German files consistent in terms of keys. After editing translation files, if the app is running, you might need to restart it to pick up changes (depending on the library, some can reload on the fly in dev). Always test in both languages after changes.

If you want to add a new language, you’d add a new locale file (say fr.json for French) and include it in the configuration (and of course, fill in all the keys). The UI might also need an update to allow selecting that language (like adding a link to /fr paths).
• Edge cases: If a translation key is missing in one language, typically the library will fallback to the default language or output the key. As a developer, check the console for warnings about missing translations if any. It’s good practice to add all keys to all supported locale files, even if one language is just a placeholder, to avoid missing text in the UI. The i18n library might offer commands or checks for missing translations (some projects use packages to find missing keys).

To illustrate, consider the Donate a habit page: The English version might have a heading “Donate a Habit” and a paragraph of instructions in English. The German page should display “Spende eine Gewohnheit” and the instructions in German. If the German text appears in English or not at all, it means either the key wasn’t translated or the app didn’t load the German locale properly. Fixing that would involve updating the de.json file or ensuring the middleware sees the de code.

In summary, the internationalization system ensures all user-facing strings are externalized in locale files, making it easy for the team to modify text or add new languages without touching template logic. As you develop, always maintain this separation: never hardcode a user-visible string in the template or code. Use a translation key. This not only aids translation but also makes it easier to tweak wording (you can just change the locale file).

Adding or Modifying Survey Questions (Forms)

One of the tasks you may encounter is updating the questions or fields in the habit donation form – for example, adding a new question, changing a prompt, or modifying the set of labels/categories. Here’s a guide on how to do that effectively:

Understanding the Current Form Structure

First, identify how the current form is built in the EJS template. Likely, the form is in the donate view and contains fields that vary by experiment group:
• In open description modes, there’s a textarea or text input for the habit description.
• In closed description modes, there might be preset options (like checkboxes or buttons) representing labels. Possibly also a text field if needed.
• In closed task modes, there is a fixed prompt (which might just be static text in the template or coming from a translation key).

The form will have an HTML structure like:

<form method="POST" action="/en/donate">
  <% if (group involves a predefined task) { %>
    <p><strong><%= __("task_prompt_text") %></strong></p>
  <% } %>
  <% if (group involves an open text entry) { %>
    <label><%= __("description_label") %></label>
    <textarea name="description"></textarea>
  <% } %>
  <% if (group involves closed/structured entry) { %>
    <label><%= __("labels_label") %></label>
    <!-- e.g., multiple checkbox inputs or select options for categories -->
    <% categories.forEach(cat => { %>
       <label><input type="checkbox" name="labels" value="<%= cat.id %>"><%= __(cat.name_key) %></label>
    <% }) %>
  <% } %>
  <button type="submit"><%= __("submit_button") %></button>
</form>

(This is pseudo-EJS code to illustrate.)

The actual code might differ, but typically you’ll see conditional blocks for each variant. Also note how it likely uses translation keys for any visible text (like labels for fields and the submit button).

Adding a New Question/Field

Suppose you want to add a new question that all users should answer, regardless of group – for example, a question like “Why do you perform this habit?” with a free-text answer: 1. Back-end Changes (Data Handling):
• Template: Add the new field in the EJS template. Since it applies to all users, you would insert it outside of any group-specific conditional (or in all relevant conditions). For example, below the existing fields, add:

<label><%= \_\_("motivation_label") %></label>
<textarea name="motivation"></textarea>

(Make sure to create translation entries for "motivation_label" in all languages, e.g., "Why do you do this?" in English and the German equivalent.)

    •	Form Submission Route: In the Express POST handler for the form, extract the new field from req.body (e.g., const motivation = req.body.motivation;). If using body-parser, it will be available as a string.
    •	SPARQL Update: Modify the SPARQL INSERT query construction to include this new field. This means adding a triple for motivation. You’ll need a predicate in the ontology for it (say :hasMotivation or similar). Ensure the ontology is updated with this property (as a DatatypeProperty of HabitEntry). Then, in the SPARQL string, include something like ; :hasMotivation "<escaped user input>" as part of the inserted data. Use proper escaping or parameterization to avoid SPARQL injection issues (at least sanitize newlines or quotes).
    •	Verify Data Model: If the ontology was updated, the Fuseki dataset should accept the new triple. If not updated, Fuseki will still store it, but it’s better to add it formally. You may restart the Fuseki container to load a changed ontology.

    2.	Front-end Changes (User Experience):
    •	Check how the new question interacts with the experimental groups. If it’s shown to all, just ensure it’s placed logically in the form. If it were meant to be group-specific, you’d instead include it in certain if-blocks only.
    •	Possibly add basic client-side validation (e.g., if you want to require an answer). HTML5 required attribute could be used, or you can rely on server-side validation.
    3.	Translations: Add keys for any new text (question labels, placeholder text, etc.) to all locale files, as mentioned. If you forget, the UI will show a missing string (likely literally the key or nothing), so don’t skip this.
    4.	Testing the Addition:
    •	Run the app and try the form in both languages and in multiple experiment conditions to ensure the new field appears where expected and that submissions with and without that field behave.
    •	Check the Fuseki data after a submission to see that the motivation text was saved as a triple. Use a SPARQL query in the Fuseki UI like SELECT ?mot WHERE { ?entry :hasMotivation ?mot } to confirm it’s there.
    •	If something isn’t working (e.g., req.body.motivation is undefined), ensure the form name matches and that the form is indeed sending it (did you include it in all conditional branches? If a user in one mode somehow doesn’t see it due to a logic bug, they won’t send it).

Modifying Existing Questions or Options

If you need to change an existing field:
• Predefined Task Text: This might be a static string or a translated text. If the experiment design changes the wording of the task instruction, simply update the translation for that prompt (e.g., change "task_prompt_text" in en.json and de.json). The template will then display the new text. No code change needed if it’s just wording.
• Labels/Categories: If the set of labels for closed data entry needs adjustment (say adding a new category or removing one), locate where these labels are defined. They could be hardcoded in the template (as a list of checkboxes) or passed in from the backend (perhaps the backend defines an array of category options). Commonly, one might keep them in a config or even in the ontology (maybe the categories are instances in RDF). However, given this is a relatively simple app, they might just be defined in the template or a simple JS object.
• To add a label: include a new checkbox/option in the form. Give it a value that corresponds to an ontology individual. Also update translations for its display name. Ensure the SPARQL insert includes logic to capture multiple labels if multiple can be selected (maybe they already handle an array from req.body.labels). If an array, you might iterate to insert multiple triples :hasCategory X for each selected label. If single-select, it’s simpler.
• To remove a label: remove that input from the template and adjust any logic in the backend that might expect it. Also, you might want to deprecate that category in the ontology or at least not use it going forward. Removing won’t break old data; those old entries will just have a category that is no longer offered to new users – which is fine.
• If these categories are also represented in RDF (likely as individuals of some Category class), consider updating the ontology to add or remove accordingly. It’s a good idea to maintain the source of truth for categories in one place (maybe the ontology file). In a more advanced setup, one could even query the RDF store for all known categories to populate the form dynamically. But that might be overkill here; probably it’s statically coded.
• Field Types: Changing a field from, say, free text to a dropdown (structured), or vice versa, can impact how data is collected. For example, if you decide that instead of open text for motivation, you want a predefined set of motivations (like a multiple choice), you’d implement that as a select input in the form, and perhaps store it as a controlled vocabulary in RDF. That’s a larger change but doable: define a MotivationCategory individuals in ontology, etc. Always weigh research needs – free text gives richer data but is unstructured, categories give easy analysis but might constrain answers.

Backward Compatibility

If you modify questions or options, consider how it affects interpreting older data:
• New fields will simply be empty on old entries (no triple). That’s fine.
• Removed fields mean old entries have data that new ones won’t. Also fine, as long as researchers know that timeline of changes.
• Changed semantics (like repurposing a field for something else) is not recommended because it confuses analysis. It’s better to introduce a new property than to change the meaning of an existing one mid-project.

Testing Changes

Every change should be tested thoroughly:
• If possible, write a unit test for the submission logic (simulate a POST with certain inputs and check that the SPARQL string contains what you expect).
• Use the application manually to ensure the UI looks correct and the data flows to the store.
• Test edge cases: what if the user leaves the new field blank (do we allow blank? if not, enforce required; if yes, handle it gracefully in SPARQL by maybe not inserting that triple or inserting an empty string literal).
• Make sure the presence or absence of the new field doesn’t break anything for different experiment groups.

By following these steps, you can confidently extend or adjust the survey questions. The key is to keep the front-end, back-end, and ontology in sync with any such change.

Data Flow: From User Input to RDF Storage

This section summarizes the end-to-end flow of data in Health Habit Hub, tying together the front-end and back-end interactions when a user donates a habit: 1. User Fills the Form (Front-End): The participant accesses the donation page (which, as described, is tailored to their assigned experimental group). They enter their habit information into the form fields provided. Depending on the group, this could be typing into a text box, selecting category labels, or both. All form fields have name attributes which will be used as keys in the submission data. For example, <textarea name="description"> for the habit description, or <input type="checkbox" name="labels" value="Exercise"> for a label. 2. Form Submission (HTTP Request): When the user clicks the submit button, the browser sends an HTTP POST request to the server. The URL is the form’s action (likely something like http://localhost:3000/en/donate with method POST). The form data is encoded (as application/x-www-form-urlencoded or multipart form data, typically). This request includes all the field values the user provided. 3. Express Server Receives Data: The Node.js Express app has a route defined to handle this POST request. Middleware like body-parser (now built into Express as express.urlencoded) will parse the form data and make it available on req.body. The route handler function is invoked with this data. For instance, req.body.description might contain the habit text, and req.body.labels might be an array of selected labels (if multiple were checked). 4. Data Processing and Validation: The server may perform some validation on the input. For example, it might check that the description isn’t empty if it’s required, or that at least one label was chosen in closed-entry mode. If a required field is missing or some validation fails, the server could respond by re-rendering the form with an error message (and not proceed to save). Assuming validation passes (and often for this kind of simple app, validation might be minimal or left to the front-end), the server proceeds to prepare the data for storage. 5. SPARQL Update Query Formation: The Express handler then constructs a SPARQL query to insert the new data into the RDF store. This involves mapping the form fields to RDF properties as discussed. It will typically create a string for the SPARQL INSERT command. If using template strings in JS, it might look like:

const desc = sanitize(req.body.description);
const entryURI = generateEntryURI(); // a function to make a new unique URI
let sparql = `  PREFIX ex: <http://example.com/health-habits#>
  INSERT DATA {
    ex:${entryURI} a ex:HabitEntry ;
      ex:hasDescription "${desc}"@${lang} ;`;
if (req.body.labels) {
// if labels is an array:
req.body.labels.forEach(label => {
sparql += ` ex:hasCategory ex:${label} ;`;
});
}
sparql += ` ex:assignedGroup "${req.session.group}" . }`;

This is a simplified illustration. In practice, the code must ensure proper escaping of quotes and special characters in user input to avoid breaking the SPARQL syntax. It might also handle multi-valued fields carefully (like adding multiple triples for each label as shown). The lang variable could be the locale of the user (so the description literal gets a language tag like @en or @de). The generateEntryURI() might create something like a UUID or a random number to ensure each entry subject URI is unique.

    6.	Sending Data to Fuseki: The constructed SPARQL query string is then sent to the Fuseki server via an HTTP request. The code will likely use the Fuseki HTTP Update API. By default, if the dataset is named (for example, let’s say the dataset is /ds), the update endpoint is POST http://fuseki:3030/ds/update with the query in the body (parameter update= or direct body if using proper content type). In Docker, fuseki:3030 is the hostname:port of the Fuseki container accessible from the app container. Since the Node app runs in the app container, it can reach the fuseki container using its service name (fuseki) thanks to Docker Compose networking. So likely an environment variable or config is set such that the app knows the endpoint URL (like FUSEKI_URL = http://fuseki:3030/ds).

The Node app can use a library like axios or node-fetch to make this POST request. It will post with appropriate headers (Content-Type: application/sparql-update or form-url-encoded with update= parameter). If using a SPARQL client library, that library will handle the details. 7. Fuseki Stores the Data: Fuseki receives the SPARQL update, executes it on its dataset. This will insert the triples into the RDF store. On success, Fuseki returns an HTTP 200 OK response (possibly with a result message, or often just empty). If there’s an error (like malformed SPARQL or a server issue), it would return a 400/500 with an error message. The Node app should check the response. In a simple implementation, if the response status is not 200, it might throw or log an error. 8. Server Responds to User: After saving data, the Node server needs to respond to the user’s browser to complete the request. There are a few possibilities:
• It could redirect the user to a new page, such as a thank-you confirmation (res.redirect('/en/thankyou') for example). Then the GET for that page could display a message. This is a common pattern to avoid form re-submission issues.
• It could render the same form page but with a flash message indicating success. However, that might risk the user hitting refresh and re-submitting; redirect-after-post is usually better.
• It might even render some of the data back (“You submitted: …”) – though that’s less likely in this scenario.
Check the actual code to see what it does. If there’s no explicit redirect, possibly it just falls through to rendering the form again. The README didn’t specify, but the focus was on the data collection rather than user feedback, so a simple “Thank you” page might exist or be something to implement if not present. 9. User Sees Confirmation: Assuming a confirmation step is in place, the user now sees a message that their habit data was received. If they stayed on the form page, perhaps now the form is cleared or they are told they can submit another (depending on whether multiple submissions are allowed – likely yes, they could submit multiple habits, though each would be a separate session if anonymity is needed, or maybe they just stay in same session and can do multiple? The design doesn’t forbid multiple from one person). 10. Data in RDF: The new habit entry now resides in the Fuseki RDF store. Researchers (or developers) can query it via SPARQL. If you go to the Fuseki web interface at http://localhost:3001/ and use the query interface, you can run a query to see the data. For example:

SELECT ?entry ?desc ?cat ?group
WHERE {
?entry a ex:HabitEntry ;
ex:hasDescription ?desc ;
ex:assignedGroup ?group .
OPTIONAL { ?entry ex:hasCategory ?cat. }
}

This would list each entry’s description, group, and category if any. The data would include the one you just submitted. This is a great way to verify end-to-end that what the user entered made it to the database correctly.

    11.	Subsequent interactions: The session still remembers the group. If the user goes back to /donate (without closing the browser or session timing out), they’ll see the same variant of form. They could submit again. Each submission would repeat the above flow, possibly generating multiple entries from one user (the system doesn’t restrict that unless explicitly coded to do so).

From this flow, you can see that data travels from a form field in the browser all the way to an RDF triple in the database. As a developer, when modifying anything in this pipeline, consider its effect on each stage:
• Change in form -> update how data is read in req.body and how SPARQL is constructed.
• Change in ontology -> update how SPARQL is constructed and maybe how the form is structured (if adding a new category, etc.).
• Change in submission handling (like adding a confirmation page) -> update what the user sees.

The system does not involve any intermediate business logic layer beyond the straightforward mapping (there’s no complex computation on the data before storing, which keeps things simpler).

One extra note: Security considerations – Because this is a research app likely used in a controlled environment, security is somewhat relaxed (no user login, data is presumably public domain). However, if this were exposed on the internet:
• We’d ensure to sanitize inputs to avoid injection attacks. SPARQL injection is a lesser-known but possible vector (someone could try to craft input that closes the string and adds additional triples). Using parameterized queries or at least escaping quotes/newlines is important.
• We might want to throttle or captcha the form if abuse is a concern (someone could script spam submissions). Probably not needed here, but something to keep in mind if scaling up.
• The Fuseki endpoint by default has no authentication; in production, one would restrict access (maybe firewalled so only the app can talk to it, which in Docker it is, since fuseki’s port 3030 might not be exposed except as 3001 for local debug – on a server you’d likely not expose that publicly).

Now you have a clear picture of how data flows through the system. This understanding will help in debugging issues (e.g., if data isn’t showing up in the DB, you know to check each step: Did the form send it? Did Express get it? Was SPARQL formed correctly? Did Fuseki accept it?).

Testing and Linting

Maintaining code quality and correctness is important, and the project provides tools to help with that. The repository includes scripts for running tests, checking code style, and linting. As a new developer, you should integrate these into your workflow. Here’s how to use them:
• Unit Tests: The project has a suite of unit tests (likely for the Node application logic). You can run the tests with:

npm run test:unitTests

This will execute the unit tests and report results ￼. The exact test framework isn’t explicitly named in documentation, but the presence of this script suggests a testing setup (possibly Jest or Mocha). Running npm test (which likely is an alias) will usually run all tests and checks. In fact, there is a script:

npm run test

which is configured to run formatting check, lint, and unit tests in sequence ￼. This is a convenient command to ensure everything is in order before committing changes. Use it regularly, especially before pushing commits or opening a pull request.

    •	Linting (ESLint): ESLint is used to catch code problems and enforce a coding style. To check for any lint issues, run:

npm run lint

This will analyze the JavaScript code for issues (undefined variables, improper usage, etc.) according to the rules set (likely there’s an .eslintrc defining these). If ESLint finds problems, they will be listed in the console with file and line numbers ￼. Many of these might be auto-fixable or minor style things. You can apply automatic fixes with:

npm run lint:fix

which will attempt to fix all fixable issues (like formatting or simple refactoring) ￼. After running that, still re-run npm run lint to ensure nothing remains. Linting helps maintain consistency (like using const vs let, spacing, etc.) and prevents certain classes of bugs.

    •	Code Formatting (Prettier): Prettier is configured to format the code in a consistent style. You can check if the code is properly formatted by running:

npm run format:check

If code is not formatted to Prettier’s rules, this will list differences ￼. Usually, it’s simpler to just run the fix:

npm run format:fix

which will auto-format the codebase according to the style rules ￼. This includes spacing, quotes, semicolons, etc. It’s often useful to run this before committing, so you don’t get style nits in code review. Some developers integrate Prettier with their editor to format on save.

    •	Integration Tests (if any): The documentation only explicitly mentions unit tests. If there are higher-level integration tests (maybe using something like Supertest to hit endpoints), they would likely also run under the npm test umbrella. Check the test folder to see what’s covered. If not, consider writing simple integration tests for routes as needed.
    •	Manual Testing: Apart from automated tests, because this application involves user interaction and a database, it’s wise to do manual testing, especially after changes:
    •	Spin up the app via Docker, try the form in a browser for both languages, and verify that expected outcomes happen (data appears in Fuseki, etc.).
    •	If possible, test on different browsers or devices to see that everything looks okay (the CSS heavy nature suggests to ensure it works on Chrome, Firefox, mobile Safari, etc., though if using standard CSS it should).
    •	Continuous Integration (CI): The repository doesn’t mention a CI setup, but if integrated (like GitHub Actions), it would probably run npm run test on each push or PR. As a team, making sure all tests pass and lint is clean before merging is important.
    •	Writing Tests for New Code: When you add features or fix bugs, it’s good practice to write corresponding tests. For example, if you implement the new “motivation” question, add a unit test for the function that builds the SPARQL query to ensure it includes the motivation text. Or a test for the route that if req.body.motivation is provided, the resulting data structure has a motivation field. Tests increase confidence that future refactoring won’t break your additions.
    •	Lint/Format on Commit: Some teams set up git hooks (e.g., using Husky) to run linting/formatting on each commit. Check if this project has any (look for a husky config or .git/hooks instructions). If not, it’s up to developers to remember to run them manually.

In short, use npm run test as your all-in-one check – it will run format check, lint, and unit tests ￼. If everything passes, you get a green light that your changes didn’t break style or functionality. If something fails:
• Format: run format:fix.
• Lint: run lint:fix or fix manually if it’s a logic issue.
• Tests: debug the failing tests, adjust code or tests accordingly.

Adhering to these ensures a clean and robust codebase, and makes onboarding easier (everyone sees a consistent style and tests describe intended behavior). The fact that these scripts are provided ￼ indicates the maintainers value these checks, so as a new contributor, you should too.

Deployment and Environment Configuration

Deploying the Health Habit Hub to an environment (server or cloud) largely involves running the Docker containers in a production setting. Here’s what to consider for deployment and how to configure various environments:

Deployment using Docker Compose

Since the application is containerized, the simplest deployment approach is to use the same Docker Compose setup (perhaps without the watch mode) on a server. The steps would be: 1. Ensure the server (or VM) has Docker and Docker Compose installed. 2. Copy the repository files to the server (or use git clone on the server). 3. Configure any environment-specific settings (see below). 4. Run docker compose up -d to start the services in the background. The -d flag detaches and runs them continuously.

This will start the app (Node.js) and fuseki containers just like in development. For production usage, you might not want the Compose Watch feature (which rebuilds on file changes). Instead, you’d run a stable configuration:
• Possibly use docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d if a separate production override file exists (for instance, to turn off watch, or to use different image tags). If there’s no separate file, you can simply run the normal compose; the watch service will rebuild on code changes but if code isn’t changing in production, it’s fine (though slight overhead). Alternatively, you could modify the compose file to remove the watch functionality (maybe by removing the x-develop extension that triggers watch, etc., if present).

Environment Variables and Configuration

Look at how configuration is handled:
• The Node app might rely on certain environment variables, for example:
• FUSEKI_ENDPOINT or similar, to know where to send SPARQL queries. In development, this could be set to http://fuseki:3030/dataset (Docker service name). If so, ensure in production the service name resolution works similarly (in Compose, it does).
• PORT for the Node app’s port (though likely it’s hardcoded to 3000, or set in compose).
• Any i18n config (maybe not via env, but some apps use DEFAULT_LANG or such).
• If there were authentication (not in this case), you’d have secrets as env variables.
• Check the docker-compose.yml for an environment: section under each service. For example, the Fuseki service might have environment variables for admin password or dataset name. If an admin password is desired in production, you would set FUSEKI_ADMIN_PASSWORD env (just as an example, Jena Fuseki can be secured with an admin account). In dev it’s likely wide open (no auth).
• Also, confirm if volumes are used: The fuseki might use a volume to store data persistently. In dev, it might not be needed (fresh start each time). In prod, you probably want a volume mount for Fuseki’s data directory so that if the container restarts, you don’t lose collected data. Check Compose file: if it’s not there, consider adding something like:

services:
fuseki:
volumes: - fuseki-data:/fuseki-base/data
volumes:
fuseki-data:

(This assumes how Fuseki is set up; consult Jena Fuseki docs for correct paths. This ensures persistence.)

    •	Networking and Domain: In production, you might not want to expose the app on port 3000 without a domain. Possibly you’d put a reverse proxy (like Nginx or Traefik) in front to route traffic from port 80/443 and handle SSL. The dev environment mentioned a “proxy” service which could be Traefik; if so, you could leverage it in prod by configuring domain names and TLS certificates. If not, a simple Nginx outside of Compose could forward requests to the app container.

For a simple setup, you can just expose port 3000 and have users go to http://<server-ip>:3000/. But for a nicer URL (and HTTPS), a proxy is recommended.
• Scaling Considerations: Likely not an issue here since this is a research app with limited usage. But note, if you ever needed multiple app instances behind a load balancer, they all talk to one Fuseki. That’s fine as long as session stickiness is handled (since session is in-memory by default, one might use a shared session store or ensure one user always hits the same app instance). However, that scenario is probably overkill for now.
• Fuseki Management: In production, keep in mind:
• If the data is sensitive or you want to restrict access, do not expose the Fuseki port to the public. In the current config, fuseki is mapped to localhost:3001 for dev convenience. In a server deployment, you might omit that port mapping entirely so it’s only accessible to the app container and not from outside. Researchers can still access it by SSH-ing to the server or temporarily tunneling if needed.
• Set a password for the Fuseki admin UI if deploying publicly (so random people can’t modify or wipe data via the UI). Jena Fuseki supports a --passwd option or a config file for credentials.
• Monitor memory usage: Fuseki keeps data in-memory/disk depending on config. For large data, you’d want to allocate sufficient RAM. In our case, data volume is probably low (text entries).
• Logging: The app prints logs to stdout (which docker captures). In production, you may want to aggregate these logs or at least periodically review them. Docker by default will log to a file (json). You can set log rotation to avoid running out of disk with logging options in Compose. The Node app might not have a verbose logger configured (maybe just console.log). If needed, consider integrating a logger library for better structured logs.
• Error handling in production: Make sure any unhandled exceptions in Node don’t crash the app or, if they do, Docker restarts it (you can add restart: always in Compose to ensure the containers restart on failure). The default Compose file might already have restart policies.

Deployment Example

Assuming you have a server ready:
• Clone the repo.
• Possibly edit docker-compose.yml:
• Remove the profiles: [watch] or any dev-specific bits. Or simply use docker compose up -d without --watch (the watch flag might be ignored or not needed outside Docker Desktop).
• (Optional) set up volumes for persistence as mentioned.
• (Optional) set environment variables for any production config (like an admin password for fuseki, etc.).
• Run docker compose up -d.
• Set up your DNS or domain to point to this server. If not using a separate proxy container with domain routing, you might install Nginx on host:
• Proxy example.com to localhost:3000 for the app, and maybe have an /fuseki path proxied to localhost:3001 if you want remote access to Fuseki (or better, keep that internal).
• Obtain an SSL certificate (with Let’s Encrypt via Certbot or use a managed service).
• Test the site via the domain. Ensure all functionalities work same as dev.

Given that internal instructions mention an internal URL (swdev.wiwi.tu-dresden.de), presumably the app has been deployed on a network server at TU Dresden for actual usage ￼. That might have been done similarly with Docker or by manually running Node and Jena on that server. We don’t have specifics, but the above guidelines hold.

Environment Configuration Summary
• Development: Mostly handled by Docker Compose with watch. Just ensure Docker resources (like memory for the VM if on Docker Desktop) are sufficient to run Node and Java comfortably.
• Testing/Staging: You could spin up the stack on a staging server the same way. If you need to test with different configurations (say, with a different dataset), you could point to a different Fuseki dataset by changing env or config. Or use an alternative compose file to connect to a test Fuseki.
• Production: Use Docker Compose (maybe in detached mode as a systemd service or via a process manager like running inside a screen or using Docker’s restart policies). Lock down Fuseki, use a domain for the app, monitor the containers.

One more note: if at some point an API or client other than the web browser is needed (for example, a mobile app sending habits), you could expose an API route in the Express app. That would then also talk to Fuseki. But currently it’s just web.

Finally, ensure to document any environment-specific variable or credentials in a secure way. For example, if an admin password is set for Fuseki, don’t hardcode it in code – use env var, and don’t commit real secrets to the repo. Use .env files or CI secrets for that. Since this is an open project, likely no secrets are needed (all data is public research data). But good to keep in mind.

Developer Tips and Common Pitfalls

Working on Health Habit Hub, especially as a new contributor, here are some tips and potential pitfalls to be aware of:
• Setting Up DNS for Dev: The dev instructions mention using addresses like app.localhost and fuseki.localhost ￼. This works on Docker Desktop for Mac because of how it handles \*.localhost domain routing. On other systems, you might need to add entries to your /etc/hosts (e.g., 127.0.0.1 app.localhost fuseki.localhost proxy.localhost) to use those addresses. If that’s troublesome, just use localhost:3000 and localhost:3001 as the README suggests ￼. The key is not to be confused if app.localhost doesn’t resolve – it’s a convenience, not a requirement.
• Apple Silicon (M1/M2 Macs): As noted, if you develop on an ARM-based Mac, the Fuseki container might have issues under x86 emulation ￼. The solution is to disable “Use Rosetta for x86/amd64 emulation” in Docker’s settings, or ensure Docker pulls an arm64 version of Fuseki. This is a one-time setup. Without it, you might find the fuseki container keeps restarting or failing on Apple Silicon.
• Session Management: The random group assignment relies on sessions (likely express-session). A common pitfall is not configuring the session secret or store in production. For dev, it might use the default memory store and a simple secret. In production, if you had multiple instances, a memory store would be an issue (but with one instance, it’s fine). Just ensure you set a SESSION_SECRET env var if required so that sessions are properly secured. If you restart the app container, all session memory is lost, meaning returning users could get re-assigned a new group (which might be fine). Just something to note – session is ephemeral here, no persistence.
• Working with RDF/SPARQL: If you’re new to semantic web tech, the learning curve can be a pitfall. Some tips:
• Use the Fuseki web interface to test your SPARQL queries. It has a nice editor (YASGUI) and can show results in a table. This helps debug queries outside of the app.
• Remember that SPARQL is case-sensitive for prefixes and requires correct URIs. A common mistake is forgetting to prefix a term. If you see no data returned for what you think should exist, perhaps you forgot a prefix or made a typo in class/property URI.
• When inserting data, ensure your syntax is exactly right. A missing semicolon or period in the SPARQL string will cause the whole query to fail. Fuseki’s error messages can sometimes pinpoint the line, sometimes not.
• Always test a new SPARQL query in the web UI or a SPARQL client before integrating into code, to confirm it does what you want.
• Ontology Mismatch: If you accidentally use a predicate or class name that isn’t in the ontology (or differently spelled), you might insert data that’s inconsistent. It won’t break Fuseki, but analysis might become harder. Stick to the terms defined in the fuseki schema file. If you change the ontology, be consistent across code and documentation.
• Internationalization Pitfalls:
• Not providing a translation for all languages is a common oversight. Always update both (or all) locale files. If not, the interface might show blank or fallback text.
• If you see something like [Object object] or a raw key on the rendered page, it could mean the translation function was used incorrectly or the key doesn’t exist. Double-check usage (for i18n library usage, referencing wrong scope or forgetting to initialize can cause that).
• Changing the structure of translation JSON (like nesting keys differently) requires updating all usage in templates. So try to keep translation keys flat and straightforward to avoid confusion.
• Prettier vs ESLint: Sometimes Prettier and ESLint might disagree on formatting if not configured to work together. However, often an ESLint config is set to defer style to Prettier. If you find lint errors about formatting, run Prettier fix, and vice versa. The provided scripts likely handle it but be aware.
• Testing Pitfalls: Ensure tests don’t rely on a running Docker services. Ideally, unit tests should mock out the Fuseki calls (or test those functions in isolation by stubbing an HTTP response). If a test actually tries to insert into Fuseki, it might fail if Fuseki isn’t running in CI. So tests probably use stubs. When writing new tests, follow existing patterns.
• Data Consistency: Since this collects research data, it’s important not to accidentally corrupt or delete data:
• Be careful with SPARQL DELETE or CLEAR commands. The app doesn’t seem to use any deletion (likely not, as data once donated is kept). If you ever need to run maintenance queries on the dataset (like removing test entries), double-check you don’t remove real data. Perhaps operate on a copy of the dataset for experiments.
• If making changes to how data is stored (ontology changes), coordinate with the team on whether and how to migrate old data. For example, if you renamed a property, you might want to run a SPARQL update to add the new property and possibly keep the old for legacy. Or at least note it.
• Performance: With small scale, performance is fine. But note that each submission triggers a new HTTP call to Fuseki. That’s trivial load unless you have thousands of users simultaneously (unlikely). If scaling up, one might consider batch inserts or parallelism. But at our level, simplicity is okay.
• Common Dev Mistakes:
• Forgetting to rebuild the Docker image when you change certain things (like if you add a new npm package, you need to rebuild the app image since the Docker container might not auto-install new deps just by watch). The compose watch does rebuild on code changes, but adding a dependency might require a down + up to trigger a fresh npm install step. So if you add a package in package.json and it’s not found, rebuild the container.
• Not exposing the right ports or using the correct URL. If you try to use the Fuseki web UI via localhost:3030 and it doesn’t respond – remember in our setup it’s 3001 externally, 3030 internally. Similarly, if you try to fetch data from the app container using localhost:3030, that won’t work inside the container – it must use fuseki:3030. These networking details can trip you up until you’re familiar with Docker’s rules.
• Cleaning up Docker: After a lot of dev, you might accumulate unused images/volumes (especially if Compose watch rebuilds often, creating intermediate images). Use docker system prune periodically to clear unused resources (careful to not remove volumes with data if you need them).
• Ethical/Data Considerations: There were issues about “age restriction” and “ethical approval”. Likely the app might need to ensure only appropriate participants use it (like over a certain age, or with consent). If implementing something like an age gate, do so carefully (perhaps a simple question “Are you over 18? yes/no” before entering). And ensure not to store personal data without consent. The app currently doesn’t ask for names or such, which is good for privacy. When modifying anything, keep it anonymous unless otherwise required.

By keeping these tips in mind, you’ll avoid common pitfalls and ensure a smooth development experience. The project is fairly straightforward but spans multiple domains (front-end, back-end, RDF, Docker), so it’s normal to hit a snag in one of them. Don’t hesitate to check documentation:
• Docker and Compose docs for env/volume syntax.
• Jena Fuseki docs ￼ for config and usage.
• Express and i18n library docs for usage details.
• And of course, your fellow team members or the repository’s issue tracker for past solutions (since we saw issues filed by Bulgy404, presumably team members discuss things there).

Useful Links and References

Below is a list of resources and references that will be helpful as you work with Health Habit Hub:
• Project Repository (GitHub): The main codebase is on GitHub at helict/health-habit-hub (you’re likely reading this documentation from there). Use the repository’s README (which this document expands upon) for a quick reference ￼ ￼. The README contains a brief overview, and pointers that we have elaborated here.
• Apache Jena Fuseki Documentation: To understand the RDF database in depth – how to configure datasets, use the SPARQL endpoints, etc. – refer to the official Fuseki docs ￼. This site covers how to start/stop Fuseki, securing it, and SPARQL query examples.
• Docker and Compose Documentation: If you’re new to Docker:
• Docker install/setup guide ￼ – ensure your environment is ready.
• Docker Compose Watch docs ￼ – explains the file-watching rebuild feature we use in development.
• General Compose docs: for understanding the docker-compose.yml syntax, how networking works, etc.
• Tip: Docker official tutorial if you need a refresher on container basics.
• Node.js & Express Resources:
• Express official docs (expressjs.com) for anything related to routing, middleware, etc.
• If session or i18n library is giving trouble, check their npm page or GitHub for usage examples.
• Node.js docs (nodejs.org) – covering any core modules you might encounter.
• EJS Templating: The official EJS documentation ￼ is useful if you want to recall syntax for loops, conditionals, includes, etc., in templates. EJS is quite straightforward, but things like partials or output escaping rules are good to know.
• Internationalization in Express: If using the i18n npm package, see its documentation on GitHub or npm (search for “i18n for Node.js”). Similarly, if it’s i18next, look up “i18next Express integration” which will have guides on setup and usage. This can help if you need to debug or extend translation features.
• SPARQL Language Reference: The W3C SPARQL 1.1 Query Language specification is the ultimate reference for SPARQL. But a more approachable resource might be tutorials on SPARQL (for example, “Learning SPARQL” book or online tutorials). If you’re writing complex queries, you might want to know about FILTER, OPTIONAL, etc. A quick reference card for SPARQL could be handy.
• Ontology Design and RDF Basics: If you need to brush up on RDF, ontologies, triples, prefixes, etc., resources include:
• RDF Primer on W3C – introduction to RDF concepts.
• OWL 2 Web Ontology Language Primer – if editing the ontology, knowing a bit of OWL (classes, properties, individuals) is useful.
• There might be an existing ontology related to habits or health behavior – not sure if we based on one. For inspiration or aligning with standards, you could search for terms in data (like maybe they used schema.org’s “Habit” or something, but likely custom).
• Prettier and ESLint: The config in the project will dictate style, but if you need to adjust or understand a rule:
• Prettier docs for its options and integration with ESLint.
• ESLint rules documentation (eslint.org) for any rule that pops up in lint warnings.
• Community and Support: Since this is likely an academic or collaborative project, don’t forget human resources:
• The repository’s Issues tab might have discussions that clarify certain design decisions or known bugs (we saw a few issues enumerated).
• The Contributors list on GitHub ￼ shows who has contributed; they might be reachable if you have specific questions.
• If this is part of a larger project or thesis, there might be internal documentation or meeting notes – check if such links are provided anywhere (for instance, maybe a Confluence or Overleaf doc if at TU Dresden).
• Similar Projects: It can also help to glance at similar habit-tracking or data donation projects to see how they do things. For instance, the Habitica open-source project (though it’s much larger and gamified), or other academic projects that collect self-report data. They might offer ideas or libraries (like using LOINC codes for health metrics, etc., but that’s beyond current scope).

Remember that keeping documentation up to date is a continuous process. As you contribute to the project, also update this guide or the README with any new instructions or changes (future developers will thank you!). This document serves as a comprehensive starting point, but living projects evolve.

Happy coding, and thank you for contributing to Health Habit Hub – your work will help drive research into healthy habits through better data collection!
