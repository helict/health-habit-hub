# Backup System Documentation

## Overview

This system provides automated daily backups of all critical data for Health Habit Hub:
- **MongoDB** - Survey responses and user data
- **Apache Jena Fuseki** - RDF/SPARQL habit donation data
- **Neo4j** - Graph database habit donation data

Backups run automatically every 24 hours and are stored locally in the `./backups/` directory.

---

## What Gets Backed Up

| Data Source | Content | Criticality |
|-------------|---------|-------------|
| MongoDB | Survey definitions, user submissions, demographics | CRITICAL |
| Fuseki | Habit donations, translations, experimental data | CRITICAL |
| Neo4j | Graph relationships, habit contexts, behaviors | CRITICAL |

---

## How It Works

The backup service:
1. Runs as a Docker container alongside other services
2. Executes backups every 24 hours automatically
3. Creates compressed archives with timestamps
4. Keeps the last 7 days of backups (configurable)
5. Automatically deletes old backups

**Backup Schedule**: Every 24 hours (starts when container is launched)

**Storage Location**: `./backups/` directory on host machine

**Retention Policy**: 7 days (configurable via `BACKUP_RETENTION_DAYS` in `.env`)

---

## Setup & Usage

### 1. Build and Start Backup Service

```bash
# Build the backup service image
docker-compose build backup

# Start all services including backup
docker-compose up -d
```

The backup service will start automatically and run backups every 24 hours.

### 2. Manual Backup (Immediate)

To trigger a backup immediately without waiting:

```bash
docker-compose run --rm backup /backup.sh
```

### 3. List Available Backups

```bash
ls -lh backups/
```

You'll see files like:
- `full_backup_20251006_143022.tar.gz` - The backup archive
- `backup_20251006_143022.manifest` - Metadata about the backup

### 4. Restore from Backup

**⚠️ WARNING: This will overwrite current data!**

```bash
# Interactive restore (will ask for confirmation)
docker-compose run --rm backup /restore.sh /backups/full_backup_20251006_143022.tar.gz

# After restore, restart services
docker-compose restart mongo fuseki neo4j
```

---

## Configuration

### Change Retention Period

Edit `.env`:
```bash
# Keep backups for 14 days instead of 7
BACKUP_RETENTION_DAYS=14
```

Then restart the backup service:
```bash
docker-compose restart backup
```

### Change Backup Schedule

To run backups more or less frequently, edit `docker-compose.yml`:

```yaml
# Run every 12 hours (43200 seconds)
command: /bin/bash -c "while true; do /backup.sh && sleep 43200; done"

# Run every 48 hours (172800 seconds)
command: /bin/bash -c "while true; do /backup.sh && sleep 172800; done"
```

---

## Monitoring

### Check Backup Status

```bash
# View backup service logs
docker-compose logs backup

# View recent backups
docker-compose run --rm backup ls -lh /backups/
```

### Check Last Backup

```bash
# View the manifest of the most recent backup
cat backups/backup_*.manifest | tail -1
```

---

## Backup File Structure

Each backup contains:
```
full_backup_YYYYMMDD_HHMMSS.tar.gz
├── mongodb/              # MongoDB dump (all collections)
├── fuseki-data.tar.gz    # Fuseki RDF data
└── neo4j-data.tar.gz     # Neo4j graph database
```

---

## Troubleshooting

### Backup Service Not Running

```bash
# Check container status
docker ps -a | grep h3-backup

# View logs for errors
docker-compose logs backup

# Restart the service
docker-compose restart backup
```

### Backup Files Too Large

If backups are consuming too much disk space:
1. Reduce retention period in `.env`
2. Manually clean old backups: `rm backups/full_backup_202410*.tar.gz`

### Restore Failed

If restore encounters errors:
1. Stop all services first: `docker-compose down`
2. Manually extract backup: `tar -xzf backups/full_backup_*.tar.gz -C /tmp/restore`
3. Inspect contents and restore manually to each database
4. Restart services: `docker-compose up -d`

---

## Best Practices

✅ **Regularly test restores** - Test recovery every month to ensure backups work

✅ **Monitor disk space** - Ensure the server has enough space for backups

✅ **External copies** - If the server is backed up by your hosting provider, you're already protected. If not, consider copying backups to another location.

✅ **Before major changes** - Run a manual backup before significant updates:
```bash
docker-compose run --rm backup /backup.sh
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Manual backup | `docker-compose run --rm backup /backup.sh` |
| List backups | `ls -lh backups/` |
| Restore backup | `docker-compose run --rm backup /restore.sh /backups/FILE.tar.gz` |
| View logs | `docker-compose logs backup` |
| Change retention | Edit `BACKUP_RETENTION_DAYS` in `.env` |

---

## Additional Server-Level Backups

Since your hosting provider already backs up the server, you have **dual protection**:

1. **Application-level backups** (this system) - Allows quick restoration of specific databases
2. **Server-level backups** (hosting provider) - Full system recovery in case of catastrophic failure

This provides defense-in-depth for your data.
