# Production Deployment Guide

## Overview

This guide covers deploying Health Habit Hub to production using Portainer on your server.

**Server Details:**
- IP: 141.76.16.16
- Domain: habit.wiwi.tu-dresden.de
- Management: Portainer
- Auto-update: Every 5 minutes from `master` branch

## Pre-Deployment Checklist

### 1. Server Prerequisites
- [ ] Server accessible at 141.76.16.16
- [ ] Portainer installed and running
- [ ] Ports 80 and 443 open in firewall
- [ ] Docker installed (managed by Portainer)

### 2. DNS Configuration
- [x] Domain `habit.wiwi.tu-dresden.de` resolves to `141.76.16.16`
- [x] DNS propagation complete (verified with `dig`)

### 3. External Services
- [ ] Google reCAPTCHA keys obtained (https://www.google.com/recaptcha/admin)
  - Site key
  - Secret key
  - Domain `habit.wiwi.tu-dresden.de` added
- [ ] Mailjet API credentials obtained (https://app.mailjet.com/account/api_keys)
  - API key
  - Secret key
  - Sender domain verified

### 4. Security
- [ ] Generate secure passwords for:
  - Fuseki admin password
  - MongoDB password
  - Mongo Express password
  - Neo4j password
  - Traefik dashboard password (use `htpasswd -nb admin your-password`)

## Portainer Deployment Steps

### Step 1: Access Portainer
1. Navigate to Portainer web interface
2. Login with your credentials
3. Select your environment

### Step 2: Create Stack
1. Go to **Stacks** → **Add stack**
2. Stack name: `health-habit-hub`
3. Build method: **Repository**

### Step 3: Configure Git Repository
- **Repository URL:** `https://github.com/helict/health-habit-hub`
- **Repository reference:** `refs/heads/master`
- **Compose path:** `docker-compose.prod.yml`
- **GitOps updates:** Enable
  - Polling interval: 5 minutes
  - Re-pull image: Enable
  - Force redeployment: Enable

### Step 4: Override Environment Variables

The `stack.env` file contains template values. Override these in Portainer:

#### Required Overrides:
```env
# Passwords (generate secure ones!)
ADMIN_PASSWORD=<your-secure-fuseki-password>
MONGO_PASSWORD=<your-secure-mongo-password>
MONGO_EXPRESS_PASSWORD=<your-secure-mongo-express-password>
NEO4J_PASSWORD=<your-secure-neo4j-password>

# Traefik Dashboard (generate: htpasswd -nb admin your-password)
TRAEFIK_DASHBOARD_AUTH=<your-htpasswd-hash>

# reCAPTCHA (from Google)
RECAPTCHA_SITEKEY=<your-production-site-key>
RECAPTCHA_SECRETKEY=<your-production-secret-key>

# Mailjet (from Mailjet dashboard)
MAIL_USER=<mailjet-api-key>
MAIL_PASS=<mailjet-secret-key>
```

#### Optional Overrides:
```env
# Backup alerts (Slack/Discord/Teams webhook)
ALERT_WEBHOOK_URL=<your-webhook-url>

# Backup retention
BACKUP_RETENTION_DAYS=14
```

### Step 5: Deploy
1. Click **Deploy the stack**
2. Wait for deployment (5-10 minutes for initial setup)
3. Monitor container logs for any errors

## Post-Deployment Verification

### 1. Check Container Status
All containers should be running:
- `h3-proxy` (Traefik)
- `h3-app` (Node.js application)
- `h3-fuseki` (RDF database)
- `h3-mongo` (MongoDB)
- `h3-mongo-express` (MongoDB web UI)
- `h3-neo4j` (Graph database)
- `h3-translate` (LibreTranslate)
- `h3-backup` (Backup service)

### 2. Verify SSL Certificate
- Check Traefik logs: Look for "certificate obtained"
- Visit https://habit.wiwi.tu-dresden.de
- Verify valid SSL certificate (green padlock)

### 3. Test Services
- [ ] Main application: https://habit.wiwi.tu-dresden.de
- [ ] Mongo Express: https://habit.wiwi.tu-dresden.de/mongo
- [ ] Fuseki (requires auth): https://habit.wiwi.tu-dresden.de/fuseki
- [ ] Translation API: https://habit.wiwi.tu-dresden.de/translate
- [ ] Neo4j browser: http://localhost:7474 (via SSH tunnel)
- [ ] Traefik dashboard: https://habit.wiwi.tu-dresden.de/dashboard

### 4. Test Backup System
Check backup logs:
```bash
docker logs h3-backup
```

Verify backup files are created:
- Location: `/backups` directory
- Format: `full_backup_YYYYMMDD_HHMMSS.tar.gz`

## Network Architecture

### How It Works
1. **External Traffic:**
   - Internet → Port 80/443 → Traefik (h3-proxy)

2. **Internal Routing:**
   - Traefik inspects Host/Path
   - Routes to appropriate service via `h3-proxy` network

3. **Service Communication:**
   - All services on `h3-proxy` bridge network
   - Services use container names (mongo, fuseki, neo4j)
   - No direct internet exposure

### Network Diagram
```
Internet
   ↓
Port 80/443
   ↓
Traefik (h3-proxy)
   ↓
h3-proxy network (bridge)
   ├── h3-app (Node.js)
   ├── h3-fuseki (RDF)
   ├── h3-mongo (MongoDB)
   ├── h3-mongo-express (MongoDB UI)
   ├── h3-neo4j (Graph) - Port 7474/7687 exposed for SSH tunnel
   ├── h3-translate (LibreTranslate)
   └── h3-backup (Backup service)
```

## Automatic Updates

### How It Works
- Portainer checks `master` branch every 5 minutes
- If changes detected:
  1. Pulls latest code
  2. Rebuilds images if needed
  3. Recreates containers
  4. Zero-downtime for config changes

### Triggering Manual Update
In Portainer:
1. Go to **Stacks** → `health-habit-hub`
2. Click **Pull and redeploy**

## Troubleshooting

### SSL Certificate Issues
**Problem:** Certificate not obtained

**Solutions:**
1. Check ports 80/443 are open:
   ```bash
   sudo ufw status
   ```
2. Verify DNS propagation:
   ```bash
   dig habit.wiwi.tu-dresden.de
   ```
3. Check Traefik logs:
   ```bash
   docker logs h3-proxy | grep -i certificate
   ```

### Services Can't Communicate
**Problem:** App can't connect to MongoDB/Fuseki/Neo4j

**Solutions:**
1. Verify all containers on same network:
   ```bash
   docker network inspect h3-proxy
   ```
2. Check service names match docker-compose.prod.yml
3. Verify environment variables in Portainer

### Backup Failures
**Problem:** Backup container shows errors

**Solutions:**
1. Check backup logs:
   ```bash
   docker logs h3-backup
   ```
2. Verify MongoDB credentials match
3. Ensure `/backups` directory has write permissions
4. Check disk space

### Container Won't Start
**Problem:** Container in restart loop

**Solutions:**
1. Check container logs:
   ```bash
   docker logs <container-name>
   ```
2. Verify environment variables set correctly
3. Check resource constraints (memory/CPU)

## Monitoring

### Container Logs
View logs in Portainer:
- **Stacks** → `health-habit-hub` → Click container → **Logs**

Or via CLI:
```bash
docker logs -f <container-name>
```

### Resource Usage
View in Portainer:
- **Containers** → Click container → **Stats**

### Backup Status
Check latest backup:
```bash
docker exec h3-backup ls -lh /backups/full_backup_*.tar.gz | tail -5
```

View backup manifest:
```bash
docker exec h3-backup cat /backups/backup_*.manifest | tail -20
```

## Maintenance

### Updating Application Code
1. Push changes to `master` branch
2. Wait 5 minutes (or trigger manual update)
3. Verify deployment in Portainer logs

### Rotating Passwords
1. Generate new secure password
2. Update in Portainer environment variables
3. Click **Update the stack**
4. Restart affected containers

### Backup Restoration
See `backup-service/restore.sh` for restoration procedures.

### Certificate Renewal
Automatic via Let's Encrypt:
- Certificates auto-renew 30 days before expiry
- Monitor Traefik logs for renewal notices

## Security Best Practices

- [ ] All passwords are strong and unique
- [ ] Traefik dashboard protected with authentication
- [ ] Regular backups verified
- [ ] Security updates applied to base images
- [ ] Logs monitored for suspicious activity
- [ ] Firewall configured (only ports 80/443 open)
- [ ] SSH key authentication enabled
- [ ] Root login disabled

## Support

### Logs Location
- Traefik: `docker logs h3-proxy`
- Application: `docker logs h3-app`
- Backups: `docker logs h3-backup`
- All others: `docker logs <container-name>`

### Health Checks
```bash
# Check all containers
docker ps

# Check network
docker network inspect h3-proxy

# Check volumes
docker volume ls | grep h3-
```

## URLs Reference

| Service | URL | Authentication |
|---------|-----|----------------|
| Main App | https://habit.wiwi.tu-dresden.de | None |
| Mongo Express | https://habit.wiwi.tu-dresden.de/mongo | Basic Auth (admin) |
| Fuseki | https://habit.wiwi.tu-dresden.de/fuseki | Basic Auth (admin) |
| Translation | https://habit.wiwi.tu-dresden.de/translate | None |
| Neo4j Browser | via SSH tunnel (see below) | Neo4j Auth |
| Traefik Dashboard | https://habit.wiwi.tu-dresden.de/dashboard | Basic Auth |

### Accessing Neo4j Browser via SSH Tunnel

Neo4j Browser requires an SSH tunnel for secure access. From your local machine:

```bash
# Create SSH tunnel (keeps connection open)
ssh -L 7474:localhost:7474 -L 7687:localhost:7687 service@habit.wiwi.tu-dresden.de

# Then access Neo4j Browser at:
# http://localhost:7474
# Username: neo4j
# Password: (from NEO4J_PASSWORD in .env)
```

Keep the terminal with the SSH tunnel open while using Neo4j Browser.

## Data Access and Management

### MongoDB Data

**Location on Server:**
- Database files: `/mnt/data/appdata/hhh/mongo/db`
- Config files: `/mnt/data/appdata/hhh/mongo/config`

**Access via Mongo Express (Web UI):**
- URL: https://habit.wiwi.tu-dresden.de/mongo
- Username: `admin` (from MONGO_EXPRESS_USER)
- Password: (from MONGO_EXPRESS_PASSWORD in .env)

**Initialization:**
MongoDB is automatically initialized on first run with:
- Database: `surveyjs`
- Collections: `surveys` (with sample survey), `results` (with sample responses)
- Initialization script: `mongo/entrypoint/surveyjs-init.js`

**Backup MongoDB:**
```bash
# Create backup
docker exec h3-mongo mongodump --username admin --password ${MONGO_PASSWORD} --authenticationDatabase admin --out /tmp/backup

# Copy backup to host
docker cp h3-mongo:/tmp/backup ./mongo-backup-$(date +%Y%m%d)
```

**Restore MongoDB:**
```bash
# Copy backup to container
docker cp ./mongo-backup-YYYYMMDD h3-mongo:/tmp/restore

# Restore
docker exec h3-mongo mongorestore --username admin --password ${MONGO_PASSWORD} --authenticationDatabase admin /tmp/restore
```

**Direct Access via CLI:**
```bash
# Connect to MongoDB shell
docker exec -it h3-mongo mongosh -u admin -p ${MONGO_PASSWORD} --authenticationDatabase admin

# List databases
show dbs

# Use surveyjs database
use surveyjs

# Show collections
show collections

# Query surveys
db.surveys.find()

# Query results
db.results.find()
```

### Neo4j Data

**Location on Server:**
- Database files: `/mnt/data/appdata/hhh/neo4j/data`
- Log files: `/mnt/data/appdata/hhh/neo4j/logs`

**Access via Browser:**
See "Accessing Neo4j Browser via SSH Tunnel" above.

**Backup Neo4j:**
```bash
# Stop Neo4j container first
docker stop h3-neo4j

# Create backup
sudo tar -czf neo4j-backup-$(date +%Y%m%d).tar.gz /mnt/data/appdata/hhh/neo4j/data

# Restart Neo4j
docker start h3-neo4j
```

**Restore Neo4j:**
```bash
# Stop Neo4j container
docker stop h3-neo4j

# Restore backup
sudo tar -xzf neo4j-backup-YYYYMMDD.tar.gz -C /

# Restart Neo4j
docker start h3-neo4j
```

**Direct Access via Cypher Shell:**
```bash
# Connect to Neo4j Cypher shell
docker exec -it h3-neo4j cypher-shell -u neo4j -p ${NEO4J_PASSWORD}

# Example queries
MATCH (n) RETURN count(n);  # Count all nodes
MATCH (n) RETURN n LIMIT 10;  # Show first 10 nodes
```

### Fuseki Data

**Location on Server:**
- RDF data: Named volume `h3-fuseki-data`

**Backup Fuseki:**
```bash
# Backup is included in automated daily backups
# Manual backup:
docker run --rm -v h3-fuseki-data:/data -v $(pwd):/backup alpine tar czf /backup/fuseki-backup-$(date +%Y%m%d).tar.gz -C /data .
```

**Restore Fuseki:**
```bash
# Restore from backup
docker run --rm -v h3-fuseki-data:/data -v $(pwd):/backup alpine tar xzf /backup/fuseki-backup-YYYYMMDD.tar.gz -C /data
```

## Additional Notes

- Backups run daily at midnight
- Backup retention: 14 days (configurable)
- All data persisted in named Docker volumes or host-mounted directories
- SSL certificates stored in `/mnt/data/appdata/hhh/traefik-certs/`
- MongoDB automatically initializes with sample survey data on first run
- Neo4j requires SSH tunnel for secure browser access
