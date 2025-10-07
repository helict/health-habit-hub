# Production Deployment Guide

## Overview

This guide covers deploying the Health Habit Hub application to production using Docker Compose with automatic SSL certificates via Let's Encrypt.

**Production Domain**: `habit.wiwi.tu-dresden.de`
**Server IP**: `141.76.16.16`

---

## Docker Compose Files

This project uses **two** Docker Compose configurations:

1. **`docker-compose.yml`** - Local development
   - HTTP only (no SSL)
   - Direct port access for debugging
   - Path-based routing on `localhost` (matches production routing)
   - Test credentials
   - Bind mounts for mongo

2. **`docker-compose.prod.yml`** - Production deployment
   - HTTPS with automatic Let's Encrypt SSL certificates
   - All traffic behind Traefik reverse proxy
   - Path-based routing on production domain
   - Named volumes for data persistence
   - Non-root container users
   - Secure passwords required

---

## Testing Locally Before Production

Before deploying to production, test your application locally using the **development** docker-compose:

### Local Testing

1. **Start the development environment**:
   ```bash
   docker-compose up -d --build
   ```

2. **Access the services** (same URL structure as production):
   - Main app: `http://localhost`
   - Traefik dashboard: `http://localhost:8080`
   - Fuseki: `http://localhost/fuseki`
   - Neo4j: `http://localhost/neo4j`
   - Translate: `http://localhost/translate`

3. **Check logs**:
   ```bash
   docker-compose logs -f
   ```

4. **Stop and cleanup**:
   ```bash
   docker-compose down
   # To remove volumes as well:
   docker-compose down -v
   ```

### Key Differences from Production

- **No SSL**: Uses HTTP instead of HTTPS (no Let's Encrypt)
- **Simple passwords**: Uses basic passwords (admin/admin) - never use these in production!
- **Direct port access**: Services expose ports for direct debugging
- **Bind mounts**: MongoDB uses local directories instead of Docker volumes

Once local testing is successful, proceed with the production deployment below.

---

## Prerequisites

### 1. DNS Configuration

Ensure the following DNS A record is configured:

```
habit.wiwi.tu-dresden.de → 141.76.16.16
```

Verify DNS propagation:
```bash
dig habit.wiwi.tu-dresden.de
nslookup habit.wiwi.tu-dresden.de
```

### 2. Firewall Configuration

Ensure these ports are open on your server (141.76.16.16):

- **Port 80** (HTTP) - Required for Let's Encrypt HTTP-01 challenge
- **Port 443** (HTTPS) - For secure HTTPS traffic
- **Port 9000** (Optional) - Portainer UI (can be restricted to specific IPs)

### 3. Server Requirements

- Docker Engine 20.10+
- Docker Compose 2.0+
- Portainer CE/BE installed
- At least 4GB RAM
- At least 20GB disk space

## Deployment Steps

### Step 1: Configure Environment Variables

1. Copy the production environment template:
   ```bash
   cp .env.production .env
   ```

2. Edit `.env` and update these critical values:

   ```bash
   # Let's Encrypt email (already set to felix.reinsch@tu-dresden.de)
   ACME_EMAIL=felix.reinsch@tu-dresden.de

   # Generate secure passwords (DO NOT use simple passwords in production!)
   ADMIN_PASSWORD=$(openssl rand -base64 32)
   MONGO_PASSWORD=$(openssl rand -base64 32)
   NEO4J_PASSWORD=$(openssl rand -base64 32)

   # Traefik Dashboard (generate with htpasswd)
   # Install htpasswd: apt-get install apache2-utils (Debian/Ubuntu) or yum install httpd-tools (RHEL/CentOS)
   # Run: echo $(htpasswd -nb admin your-secure-password) | sed -e s/\\$/\\$\\$/g
   TRAEFIK_DASHBOARD_AUTH=admin:hashed-password-here

   # Configure your reCAPTCHA keys from Google
   # IMPORTANT: Create production keys at https://www.google.com/recaptcha/admin/create
   # Add domain: habit.wiwi.tu-dresden.de
   # The TEST keys in .env will NOT work in production!
   RECAPTCHA_SITEKEY=your-production-site-key
   RECAPTCHA_SECRETKEY=your-production-secret-key

   # Configure Mailjet credentials from https://app.mailjet.com/account/api_keys
   MAIL_USER=your-mailjet-api-key
   MAIL_PASS=your-mailjet-secret-key
   MAIL_FROM=noreply@wiwi.tu-dresden.de
   MAIL_RECEIVER=felix.reinsch@tu-dresden.de
   ```

### Step 2: Deploy with Portainer

#### Option A: Deploy via Portainer Git Repository

1. Log in to Portainer at `http://141.76.16.16:9000`

2. Navigate to **Stacks** → **Add stack**

3. Configure the stack:
   - **Name**: `health-habit-hub`
   - **Build method**: Git Repository
   - **Repository URL**: `https://github.com/[your-username]/health-habit-hub`
   - **Repository reference**: `refs/heads/master`
   - **Compose path**: `docker-compose.prod.yml`

4. Add environment variables from your `.env` file in the **Environment variables** section

5. Enable **Re-pull image** and **Prune services** options

6. Click **Deploy the stack**

#### Option B: Deploy via Portainer Web Editor

1. Log in to Portainer

2. Navigate to **Stacks** → **Add stack**

3. Configure the stack:
   - **Name**: `health-habit-hub`
   - **Build method**: Web editor
   - Paste contents of `docker-compose.prod.yml`

4. Add environment variables from `.env` file

5. Click **Deploy the stack**

### Step 3: Configure reCAPTCHA (Required)

Before deployment, you **must** configure production reCAPTCHA keys:

1. **Create reCAPTCHA keys**:
   - Go to https://www.google.com/recaptcha/admin/create
   - Label: `Health Habit Hub - Production`
   - reCAPTCHA type: Choose based on your implementation (likely v2 or v3)
   - Domains: Add `habit.wiwi.tu-dresden.de`
   - Submit

2. **Update .env file**:
   ```bash
   RECAPTCHA_SITEKEY=your-actual-site-key-from-google
   RECAPTCHA_SECRETKEY=your-actual-secret-key-from-google
   ```

3. **Important**: The test keys in the development `.env` file will **not work** in production:
   - Test Site Key: `6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI`
   - Test Secret Key: `6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe`

   These only work on `localhost` and will fail on your production domain.

### Step 4: Verify Deployment

1. **Check container status**:
   ```bash
   docker ps
   ```

   All containers should show "Up" status:
   - h3-proxy (Traefik)
   - h3-app
   - h3-fuseki
   - h3-mongo
   - h3-neo4j
   - h3-translate

2. **Check Traefik logs**:
   ```bash
   docker logs h3-proxy
   ```

   Look for successful certificate acquisition:
   ```
   time="..." level=info msg="Certificate obtained for domain habit.wiwi.tu-dresden.de"
   ```

3. **Test HTTPS**:
   ```bash
   curl -I https://habit.wiwi.tu-dresden.de
   ```

   Should return `HTTP/2 200` with valid SSL certificate

4. **Access the application**:
   - Main app: `https://habit.wiwi.tu-dresden.de`
   - Traefik dashboard: `https://habit.wiwi.tu-dresden.de/dashboard/`
   - Fuseki: `https://habit.wiwi.tu-dresden.de/fuseki`
   - Neo4j: `https://habit.wiwi.tu-dresden.de/neo4j`

### Step 5: Initial Database Setup

1. **Access Fuseki** to verify RDF database:
   ```bash
   curl -u admin:YOUR_ADMIN_PASSWORD https://habit.wiwi.tu-dresden.de/fuseki/$/datasets
   ```

2. **Access Neo4j** to initialize graph database:
   - Navigate to `https://habit.wiwi.tu-dresden.de/neo4j`
   - Login with credentials from `.env`
   - Run initialization scripts if needed

## Networking Architecture

```
Internet (Port 80/443)
    ↓
Traefik Reverse Proxy (h3-proxy)
    ↓
Docker Network: h3-proxy (bridge)
    ├── h3-app (Node.js) → Port 3000
    ├── h3-fuseki (Apache Jena) → Port 3030
    ├── h3-mongo (MongoDB) → Port 27017
    ├── h3-neo4j (Neo4j) → Port 7474/7687
    └── h3-translate (LibreTranslate) → Port 5000
```

### Key Features

- **Automatic HTTPS**: Let's Encrypt certificates automatically obtained and renewed
- **HTTP → HTTPS Redirect**: All HTTP traffic redirected to HTTPS
- **Path-based Routing**: Services accessible via subdirectories
- **Internal Network**: Containers communicate via Docker network (no exposed ports except 80/443)
- **Volume Persistence**: Data persisted in named Docker volumes

## SSL Certificate Management

### Certificate Location

Certificates are stored in the Docker volume `h3-traefik-certs`:
```bash
docker volume inspect h3-traefik-certs
```

### Certificate Renewal

Let's Encrypt certificates are valid for 90 days. Traefik automatically renews them 30 days before expiration.

Monitor renewal in Traefik logs:
```bash
docker logs -f h3-proxy | grep -i certificate
```

### Troubleshooting Certificates

If certificates fail to generate:

1. **Verify DNS is correct**:
   ```bash
   nslookup habit.wiwi.tu-dresden.de
   ```

2. **Ensure port 80 is accessible** (required for HTTP-01 challenge):
   ```bash
   curl -I http://habit.wiwi.tu-dresden.de
   ```

3. **Check rate limits**: Let's Encrypt has rate limits (50 certificates per domain per week)

4. **Use staging environment for testing**:
   Edit `docker-compose.prod.yml` and add:
   ```yaml
   - --certificatesresolvers.letsencrypt.acme.caserver=https://acme-staging-v02.api.letsencrypt.org/directory
   ```

## Maintenance

### Update Application

To update from the master branch:

1. In Portainer, go to **Stacks** → **health-habit-hub**
2. Click **Pull and redeploy**
3. Or use CLI:
   ```bash
   cd /path/to/health-habit-hub
   git pull origin master
   docker-compose -f docker-compose.prod.yml pull
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Backup Data

Backup all persistent volumes:
```bash
docker run --rm \
  -v h3-fuseki-data:/data/fuseki \
  -v h3-mongo-data:/data/mongo \
  -v h3-neo4j-data:/data/neo4j \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/backup-$(date +%Y%m%d-%H%M%S).tar.gz /data
```

### View Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker logs -f h3-app
docker logs -f h3-proxy
docker logs -f h3-mongo
```

### Restart Services

```bash
# Restart all
docker-compose -f docker-compose.prod.yml restart

# Restart specific service
docker restart h3-app
```

## Security Considerations

1. **Non-Root Containers**: All containers run as non-root users for security:
   - App: runs as `node` user (from Dockerfile)
   - Fuseki: runs as `fuseki` user (UID 9008)
   - MongoDB: runs as `mongodb` user (UID 999)
   - Neo4j: runs as `neo4j` user (UID 7474)
   - LibreTranslate: runs as `libretranslate` user (UID 1032)

2. **Change Default Passwords**: Ensure all passwords in `.env` are changed from defaults
   - Use strong, randomly generated passwords (minimum 32 characters)
   - Never use passwords like "admin" or "password" in production

3. **reCAPTCHA**: Production requires real keys from Google
   - Test keys from development `.env` will NOT work
   - Create production keys at https://www.google.com/recaptcha/admin
   - Add domain: `habit.wiwi.tu-dresden.de`

4. **Traefik Dashboard**: Protected with basic auth, consider IP whitelisting

5. **Database Access**: MongoDB and Neo4j only accessible within Docker network

6. **Regular Updates**: Keep Docker images updated

7. **Firewall**: Restrict access to non-public services

8. **Backups**: Regular automated backups of volumes

9. **Let's Encrypt Email**: Set to `felix.reinsch@tu-dresden.de` for certificate notifications

## Troubleshooting

### Application not accessible

1. Check container status: `docker ps`
2. Check Traefik logs: `docker logs h3-proxy`
3. Verify DNS: `dig habshare.habconnect.wiwi.tu-dresden.de`
4. Test port 80/443: `telnet 141.76.16.16 80`

### Certificate issues

1. Check ACME logs: `docker logs h3-proxy | grep acme`
2. Verify domain resolves to correct IP
3. Ensure port 80 is open for HTTP challenge
4. Check Let's Encrypt rate limits

### Service not starting

1. Check logs: `docker logs h3-[service-name]`
2. Verify environment variables in `.env`
3. Check disk space: `df -h`
4. Check memory: `free -m`

### Database connection issues

1. Verify services are on same network: `docker network inspect h3-proxy`
2. Check environment variables for connection strings
3. Review application logs: `docker logs h3-app`

## Support

For issues or questions:
- Check logs in Portainer UI
- Review GitHub repository issues
- Contact system administrator

## URLs Reference

- **Main Application**: https://habit.wiwi.tu-dresden.de
- **Traefik Dashboard**: https://habit.wiwi.tu-dresden.de/dashboard/
- **Fuseki (RDF Database)**: https://habit.wiwi.tu-dresden.de/fuseki
- **Neo4j Browser**: https://habit.wiwi.tu-dresden.de/neo4j
- **Translation API**: https://habit.wiwi.tu-dresden.de/translate
