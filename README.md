# Health Habit Hub

<img src="./app/public/pics/h3-logo.png" width="250" alt="Health Habit Hub Logo"/>

**Production URL**: https://habit.wiwi.tu-dresden.de
**Version**: 1.0.0 (October 2025)

A research-focused web application for collecting and analyzing health habit data using a 2×2 experimental design with multi-database architecture.

---

## Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/health-habit-hub.git
cd health-habit-hub

# Configure environment
cp .env.example .env

# Start development environment
docker-compose up -d --build

# Access application
open http://localhost
```

---

## Key Features

- **Experimental Design**: 2×2 factorial design for habit data collection
- **Multi-Database**: Apache Fuseki (RDF), Neo4j (Graph), MongoDB (Documents)
- **Multi-Language**: English, German, Japanese (i18n)
- **Automated Backups**: Daily backups with 14-day retention
- **Production-Ready**: Docker Compose with automatic SSL via Let's Encrypt
- **Translation API**: Integrated LibreTranslate for multilingual content

---

## Architecture

```
Internet (80/443) → Traefik (SSL) → Node.js App → Databases
                                          ├── Apache Fuseki (RDF)
                                          ├── Neo4j (Graph)
                                          ├── MongoDB (Documents)
                                          └── LibreTranslate (API)
```

**Services**:
- **app**: Node.js/Express application
- **fuseki**: Apache Jena Fuseki (RDF triple store)
- **neo4j**: Neo4j graph database
- **mongo**: MongoDB document store
- **translate**: LibreTranslate API
- **proxy**: Traefik reverse proxy
- **backup**: Automated backup service

---

## Documentation

**Complete documentation available in [DOCUMENTATION.md](DOCUMENTATION.md)**

### Quick Links

- [Quick Start Guide](DOCUMENTATION.md#quick-start)
- [Architecture & Design](DOCUMENTATION.md#architecture--design)
- [Development Guide](DOCUMENTATION.md#development-guide)
- [Production Deployment](DOCUMENTATION.md#production-deployment)
- [Backup System](DOCUMENTATION.md#backup-system)
- [Testing](DOCUMENTATION.md#testing)
- [User Manual](DOCUMENTATION.md#user-manual)
- [Troubleshooting](DOCUMENTATION.md#troubleshooting)
- [API Reference](DOCUMENTATION.md#api-reference)

---

## Local Development

```bash
# Start with hot-reload
docker-compose watch

# View logs
docker-compose logs -f

# Run tests
cd app && npm test

# Code quality
npm run lint
npm run format
```

**Access**:
- App: http://localhost
- Traefik: http://localhost:8080
- Fuseki: http://localhost/fuseki
- Neo4j: http://localhost/neo4j

---

## Production Deployment

See [Production Deployment Guide](DOCUMENTATION.md#production-deployment) for complete instructions.

**Quick deployment**:
1. Configure DNS: `habit.wiwi.tu-dresden.de → 141.76.16.16`
2. Open firewall ports: 80, 443
3. Configure `.env` with production credentials
4. Deploy via Portainer with `docker-compose.prod.yml`
5. Verify SSL certificate obtained automatically

**Production URL**: https://habit.wiwi.tu-dresden.de

### Accessing Databases in Production

**Neo4j Browser** (requires SSH tunnel):
```bash
# Create secure tunnel to Neo4j
ssh -L 7474:localhost:7474 -L 7687:localhost:7687 service@141.76.16.16

# Then access: http://localhost:7474
# Login with Neo4j credentials (username: neo4j, password from NEO4J_PASSWORD)
```

See [DEPLOYMENT.md - Neo4j SSH Tunnel](DEPLOYMENT.md#accessing-neo4j-browser-via-ssh-tunnel) for detailed instructions.

**Other services** (available via https://habit.wiwi.tu-dresden.de):
- Mongo Express: `/mongo`
- Fuseki RDF: `/fuseki`
- Traefik Dashboard: `/dashboard`

---

## Tech Stack

**Backend**: Node.js 22, Express.js, EJS
**Databases**: Apache Fuseki (RDF), Neo4j, MongoDB
**Infrastructure**: Docker, Traefik, Let's Encrypt
**Tools**: LibreTranslate, reCAPTCHA, Mailjet

---

## Requirements

- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum (8GB recommended)
- Ports 80, 443 (production)

---

## Support

**Documentation**: [DOCUMENTATION.md](DOCUMENTATION.md)
**Issues**: https://github.com/felixreinsch/health-habit-hub/issues
**Contact**: felix.reinsch@tu-dresden.de

---

## License

Proprietary software for research purposes at TU Dresden.

**Contact**: felix.reinsch@tu-dresden.de
