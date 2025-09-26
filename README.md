# Health Habit Hub

<img src="./app/public/pics/h3-logo.png" width="250" alt="Health Habit Hub Logo"/>

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Development](#development)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Technical Stack](#technical-stack)
- [License](#license)

## Overview

Health Habit Hub is a research-focused web application designed to collect valuable habit data from users for scientific purposes. The platform employs a sophisticated 2×2 experimental design that randomly assigns users to different data entry experiences, enabling researchers to study the impact of various interface designs on data quality and user behavior.

### Research Purpose

This application serves as a data collection platform for studying:
- How participants define and report their habits
- The impact of instruction specificity on response quality
- Context-dependent habit formation patterns
- Behavioral change intervention strategies

The collected data is stored in a semantic RDF database to facilitate machine learning analysis and habit research.

## Features

### Core Functionality

- **Multi-modal Data Entry**: Four distinct experimental conditions
  - **Closed Task, Closed Description**: Predefined tasks with structured labeling
  - **Closed Task, Open Description**: Specific tasks with free-form responses
  - **Open Task, Closed Description**: Free choice tasks with structured labeling
  - **Open Task, Open Description**: Complete freedom in task and description

- **Habit Context Analysis**: Comprehensive context categorization including:
  - Temporal contexts (time-based triggers)
  - Physical settings (location-based cues)
  - Social contexts (interpersonal influences)
  - Prior behaviors (behavioral chains)
  - Internal states (emotional/physiological triggers)

- **Internationalization**: Full multilingual support (English, German, Japanese)
- **Survey Integration**: SurveyJS-powered dynamic questionnaires
- **Real-time Translation**: LibreTranslate integration for multilingual content

### Technical Features

- **Semantic Data Storage**: RDF triples in Apache Jena Fuseki
- **Containerized Architecture**: Docker-based microservices
- **Reverse Proxy**: Traefik for service routing and load balancing
- **Data Persistence**: MongoDB for survey data, Fuseki for semantic data
- **Development Workflow**: Hot-reload with Docker Compose Watch

## Architecture

The application follows a microservices architecture with the following components:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │    │   Traefik       │    │   Node.js App   │
│   (Client)      │◄──►│   (Proxy)       │◄──►│   (Express)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                       ┌─────────────────┐             │
                       │   LibreTranslate│◄────────────┤
                       │   (Translation) │             │
                       └─────────────────┘             │
                                                        │
                       ┌─────────────────┐             │
                       │   MongoDB       │◄────────────┤
                       │   (Survey Data) │             │
                       └─────────────────┘             │
                                                        │
                       ┌─────────────────┐             │
                       │   Apache Fuseki │◄────────────┤
                       │   (RDF Store)   │             │
                       └─────────────────┘             │
                                                       │
                       ┌─────────────────┐             │
                       │     Neo4j       │◄────────────┘
                       │ (Graph Store)   │
                       └─────────────────┘
```

### Service Components

1. **App Service** - Main Node.js/Express application
2. **Fuseki Service** - Apache Jena Fuseki RDF triple store (default habit storage)
3. **Neo4j Service** - Optional graph database for habit storage
4. **MongoDB Service** - Document database for survey responses
5. **Traefik Proxy** - Reverse proxy and load balancer
6. **LibreTranslate** - Open-source translation service

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (version 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0+)
- Git

### Platform-Specific Notes

**macOS with Apple Silicon (M1/M2)**: 
Disable Rosetta emulation in Docker Desktop settings to ensure proper Fuseki container operation.

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/health-habit-hub.git
   cd health-habit-hub
   ```

2. **Environment configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your specific configuration
   ```

3. **Start the application**
   ```bash
   # Development mode with file watching
   docker compose watch
   
   # Or standard mode
   docker compose up -d
   ```

4. **Access the services**
   - **Main Application**: http://app.localhost or http://localhost:3000
   - **Fuseki Database**: http://fuseki.localhost or http://localhost:3030
   - **Traefik Dashboard**: http://proxy.localhost or http://localhost:8080
   - **Translation Service**: http://translate.localhost or http://localhost:5000

## Usage

### Basic Usage

1. **Navigate to the donation page**: `/donate` or `/{language}/donate`
2. **Automatic group assignment**: Users are randomly assigned to one of four experimental groups
3. **Complete the habit entry**: Fill out the form according to your assigned interface
4. **Submit your data**: Habit data is stored in the configured graph backend (Fuseki by default, Neo4j optional)

### Graph Backend (Fuseki vs Neo4j)

You can switch the habit-donation storage between Fuseki (RDF) and Neo4j (property graph) without affecting surveys (MongoDB) or cookies.

- Toggle via env var: `GRAPH_BACKEND=fuseki|neo4j`
- Env for Neo4j: `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`
- Docker Compose includes a `neo4j` service (ports 7474/7687)

When `GRAPH_BACKEND=neo4j`, the app writes donation nodes and relationships:
- Nodes: `Habit`, `Context`, `Behavior`, `Donor`, `ExperimentalSetting`
- Rels: `DONATES`, `HAS_BEHAVIOR`, `HAS_CONTEXT`, `PART_OF`, `HAS_TRANSLATION`

### Language Support

Access the application in different languages:
- English: `/en/donate`
- German: `/de/donate`
- Japanese: `/ja/donate`

### Manual Group Testing

For development and testing purposes, you can manually specify a group:
- `/donate?group=closed_task_closed_desc`
- `/donate?group=closed_task_open_desc`
- `/donate?group=open_task_closed_desc`
- `/donate?group=open_task_open_desc`

### Survey System

Dynamic surveys can be created and accessed via:
- Survey creation interface
- Direct survey access: `/survey/{survey-id}`
- Multi-language survey support

## Development

### Development Environment

The project uses Docker Compose with file watching for rapid development:

```bash
# Start development environment
docker compose watch

# View logs
docker compose logs -f app

# Access a container shell
docker exec -it h3-app bash
```

### Code Quality Tools

```bash
# Navigate to app directory
cd app

# Format checking
npm run format:check

# Auto-format code
npm run format:fix

# Lint checking
npm run lint

# Auto-fix lint issues
npm run lint:fix

# Run unit tests
npm run test:unitTests

# Run all checks (format, lint, tests)
npm run test
```

### Project Structure

```
health-habit-hub/
├── app/                    # Main Node.js application
│   ├── controllers/        # Route controllers
│   ├── models/            # Data models
│   ├── routes/            # Express routes
│   ├── views/             # EJS templates
│   ├── public/            # Static assets
│   ├── middleware/        # Custom middleware
│   ├── utils/             # Utility functions
│   └── language/          # Internationalization files
├── fuseki/                # RDF database configuration
│   ├── Dockerfile
│   └── init/              # Initial data and schema
├── mongo/                 # MongoDB configuration
│   ├── config/
│   ├── data/
│   └── entrypoint/
├── docs/                  # Documentation
└── docker-compose.yml     # Service orchestration
```

### Key Development Files

- `app/app.js` - Main application entry point
- `app/controllers/surveyController.js` - Survey handling logic
- `app/models/survey.js` - MongoDB survey model
- `app/utils/localization.js` - Internationalization utilities
- `docker-compose.yml` - Service configuration

## API Documentation

### Core Endpoints

#### Habit Donation
- `GET /{lang}/donate` - Render habit donation form
- `POST /{lang}/donate` - Submit habit data

#### Survey System
- `GET /survey/{id}` - Render specific survey
- `POST /survey/{id}` - Submit survey response

#### Utility Endpoints
- `GET /{lang}/about` - About page
- `GET /{lang}/contact` - Contact page
- `GET /{lang}/privacy` - Privacy policy
- `GET /{lang}/accessibility` - Accessibility information

### SPARQL Integration

The application stores habit data as RDF triples using SPARQL queries. Example data structure:

```turtle
@prefix ex: <http://example.com/health-habits#> .

ex:entry_123456 a ex:HabitEntry ;
    ex:hasDescription "I drink water when I wake up"@en ;
    ex:hasCategory ex:Hydration ;
    ex:hasTimeContext ex:Morning ;
    ex:assignedGroup "open_task_closed_desc" ;
    ex:submittedAt "2025-08-26T10:30:00Z"^^xsd:dateTime .
```

## Deployment

### Production Deployment

1. **Configure environment variables**
   ```bash
   # Create production .env file
   NODE_ENV=production
   ADMIN_PASSWORD=secure_password
   APP_HOST_PORT=3000
   FUSEKI_HOST_PORT=3030
   ```

2. **Deploy with Docker Compose**
   ```bash
   # Production deployment
   docker compose -f docker-compose.yml up -d
   ```

3. **Security Considerations**
   - Set strong admin passwords
   - Configure firewall rules
   - Use HTTPS in production
   - Restrict Fuseki access
   - Regular backups of data volumes

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NODE_ENV` | Application environment | `development` |
| `APP_HOST_PORT` | App container port | `3000` |
| `FUSEKI_HOST_PORT` | Fuseki container port | `3030` |
| `ADMIN_PASSWORD` | Fuseki admin password | `admin` |
| `MONGO_USER` | MongoDB username | `admin` |
| `MONGO_PASSWORD` | MongoDB password | `admin` |
| `GRAPH_BACKEND` | Habit storage backend | `fuseki` |
| `NEO4J_URI` | Neo4j Bolt URI | `bolt://neo4j:7687` |
| `NEO4J_USER` | Neo4j username | `neo4j` |
| `NEO4J_PASSWORD` | Neo4j password | `password` |

## Contributing

### Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `npm run test`
5. Commit changes: `git commit -m 'Add amazing feature'`
6. Push to branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Development Guidelines

- Follow the existing code style (enforced by Prettier/ESLint)
- Write comprehensive tests for new features
- Update documentation for significant changes
- Ensure all experimental groups work with your changes
- Test in multiple languages when applicable

### Code Style

- Use ESLint and Prettier configurations
- Follow Node.js best practices
- Write semantic, accessible HTML
- Use meaningful commit messages

## Technical Stack

### Backend Technologies
- **Node.js** - Runtime environment
- **Express.js** - Web application framework
- **EJS** - Templating engine
- **Apache Jena Fuseki** - RDF triple store
- **MongoDB** - Document database
- **SPARQL** - RDF query language

### Frontend Technologies
- **HTML5/CSS3** - Structure and styling
- **Bootstrap** - UI framework
- **JavaScript** - Client-side functionality
- **SurveyJS** - Dynamic survey generation
- **D3.js** - Data visualization

### DevOps & Tools
- **Docker & Docker Compose** - Containerization
- **Traefik** - Reverse proxy
- **LibreTranslate** - Translation service
- **ESLint** - Code linting
- **Prettier** - Code formatting
- **Jest/Mocha** - Testing framework

### External Services
- **DeepL** - Professional translation API
- **reCAPTCHA** - Spam protection
- **Nodemailer** - Email functionality

## Research & Academic Use

This application is designed for academic research in habit formation and behavioral science. Key research features:

- **Experimental Design**: 2×2 factorial design for comparing interface effects
- **Data Integrity**: Consistent group assignment per session
- **Semantic Storage**: RDF format for advanced analysis
- **Privacy Compliance**: Anonymous data collection
- **Multilingual Support**: Cross-cultural research capability

### Citations

When using this tool for research, please cite:

```bibtex
@software{health_habit_hub,
  title={Health Habit Hub: A Research Platform for Habit Data Collection},
  author={[Authors]},
  year={2025},
  url={https://github.com/yourusername/health-habit-hub}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- TU Dresden for research support
- Apache Foundation for Jena Fuseki
- SurveyJS team for survey components
- LibreTranslate project for translation services

---

For additional information, please refer to the [detailed documentation](docs/) or contact the development team.
