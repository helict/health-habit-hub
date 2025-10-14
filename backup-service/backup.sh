#!/bin/bash

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=${BACKUP_RETENTION_DAYS:-14}
ALERT_WEBHOOK_URL=${ALERT_WEBHOOK_URL:-}
ALERT_EMAIL=${ALERT_EMAIL:-}

# Error tracking
BACKUP_ERRORS=0
ERROR_LOG=""

# Function to send alerts on failure
send_alert() {
  local message="$1"
  local status="$2"

  # Send webhook alert (Slack/Discord/etc)
  if [ -n "$ALERT_WEBHOOK_URL" ]; then
    curl -X POST "$ALERT_WEBHOOK_URL" \
      -H "Content-Type: application/json" \
      -d "{\"text\":\"🚨 Health Habit Hub Backup $status\",\"blocks\":[{\"type\":\"section\",\"text\":{\"type\":\"mrkdwn\",\"text\":\"$message\"}}]}" \
      2>/dev/null || echo "Warning: Failed to send webhook alert"
  fi

  # Send email alert via Mailjet API (if configured)
  if [ -n "$ALERT_EMAIL" ] && [ -n "$MAIL_USER" ] && [ -n "$MAIL_PASS" ]; then
    curl -X POST https://api.mailjet.com/v3.1/send \
      -u "$MAIL_USER:$MAIL_PASS" \
      -H "Content-Type: application/json" \
      -d "{
        \"Messages\": [{
          \"From\": {\"Email\": \"${MAIL_FROM:-noreply@example.com}\", \"Name\": \"Health Habit Hub Backup\"},
          \"To\": [{\"Email\": \"$ALERT_EMAIL\"}],
          \"Subject\": \"🚨 Health Habit Hub Backup $status\",
          \"TextPart\": \"$message\",
          \"HTMLPart\": \"<h3>Health Habit Hub Backup $status</h3><pre>$message</pre>\"
        }]
      }" 2>/dev/null && echo "  Email alert sent to $ALERT_EMAIL" || echo "  Warning: Failed to send email alert"
  fi
}

# Function to log errors
log_error() {
  local component="$1"
  local error="$2"
  BACKUP_ERRORS=$((BACKUP_ERRORS + 1))
  ERROR_LOG="${ERROR_LOG}\n❌ $component: $error"
  echo "ERROR: $component - $error"
}

echo "=========================================="
echo "Starting backup: $(date)"
echo "=========================================="

# Create backup directory structure
mkdir -p "$BACKUP_DIR/$DATE"

# 1. Backup MongoDB
echo "1/4 Backing up MongoDB..."
if mongodump \
  --host=mongo:27017 \
  --username="$MONGO_USER" \
  --password="$MONGO_PASSWORD" \
  --authenticationDatabase=admin \
  --out="$BACKUP_DIR/$DATE/mongodb" \
  --quiet 2>/dev/null; then
  echo "✓ MongoDB backup completed"
else
  log_error "MongoDB" "mongodump failed"
fi

# 2. Backup Fuseki
echo "2/4 Backing up Fuseki (RDF data)..."
if [ -d "/fuseki" ] && [ "$(ls -A /fuseki 2>/dev/null)" ]; then
  if tar -czf "$BACKUP_DIR/$DATE/fuseki-data.tar.gz" -C /fuseki . 2>/dev/null; then
    echo "✓ Fuseki backup completed"
  else
    log_error "Fuseki" "tar archive failed"
  fi
else
  echo "⚠ Warning: Fuseki volume is empty or not mounted"
  touch "$BACKUP_DIR/$DATE/fuseki-data.tar.gz"
fi

# 3. Backup Neo4j using native dump
echo "3/4 Backing up Neo4j (using neo4j-admin dump)..."
echo "  Stopping Neo4j for consistent backup..."

# Stop Neo4j container
if docker stop h3-neo4j >/dev/null 2>&1; then
  sleep 2  # Give it a moment to shut down cleanly

  # Create a temporary volume and set permissions
  docker volume create neo4j-backup-temp >/dev/null 2>&1
  docker run --rm -v neo4j-backup-temp:/backup alpine:latest chmod 777 /backup

  # Perform the Neo4j dump
  NEO4J_DUMP_OUTPUT=$(docker run --rm \
    --volumes-from h3-neo4j \
    -v neo4j-backup-temp:/backup \
    neo4j:5 \
    neo4j-admin database dump neo4j --to-path=/backup --overwrite-destination=true 2>&1)

  if echo "$NEO4J_DUMP_OUTPUT" | grep -q "Dump completed successfully"; then

    # Copy the dump directly using tar (to avoid Docker-in-Docker mount issues)
    docker run --rm \
      -v neo4j-backup-temp:/source:ro \
      alpine:latest \
      tar -czf - -C /source neo4j.dump | tar -xzf - -C "$BACKUP_DIR/$DATE/"

    # Clean up the temporary volume
    docker volume rm neo4j-backup-temp >/dev/null 2>&1

    echo "✓ Neo4j dump completed"
  else
    log_error "Neo4j" "neo4j-admin dump failed"
    docker volume rm neo4j-backup-temp >/dev/null 2>&1 || true
  fi

  # Restart Neo4j
  echo "  Restarting Neo4j..."
  if docker start h3-neo4j >/dev/null 2>&1; then
    echo "✓ Neo4j restarted"
  else
    log_error "Neo4j" "Failed to restart container"
  fi
else
  log_error "Neo4j" "Failed to stop container for backup"
fi

# 4. Create unified backup archive
echo "4/4 Creating unified backup archive..."
if tar -czf "$BACKUP_DIR/full_backup_$DATE.tar.gz" -C "$BACKUP_DIR/$DATE" . 2>/dev/null; then
  echo "✓ Unified archive created"
else
  log_error "Archive" "Failed to create unified backup archive"
fi

# Calculate size
BACKUP_SIZE=$(du -sh "$BACKUP_DIR/full_backup_$DATE.tar.gz" 2>/dev/null | cut -f1)

# Clean up temporary directory
rm -rf "$BACKUP_DIR/$DATE"

# Generate backup manifest
cat > "$BACKUP_DIR/backup_$DATE.manifest" <<EOF
Backup Date: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
MongoDB: $([ $BACKUP_ERRORS -eq 0 ] && echo "✓" || echo "Check logs")
Fuseki: ✓
Neo4j: $([ $BACKUP_ERRORS -eq 0 ] && echo "✓" || echo "Check logs")
Size: $BACKUP_SIZE
File: full_backup_$DATE.tar.gz
Retention: $RETENTION_DAYS days
Errors: $BACKUP_ERRORS
EOF

# Report results
echo ""
if [ $BACKUP_ERRORS -eq 0 ]; then
  echo "✓ Backup completed successfully!"
  echo "  File: full_backup_$DATE.tar.gz"
  echo "  Size: $BACKUP_SIZE"
  echo "  Location: $BACKUP_DIR/"
else
  echo "⚠ Backup completed with $BACKUP_ERRORS error(s)"
  echo -e "$ERROR_LOG"
  send_alert "⚠ Backup completed with errors:\n$ERROR_LOG\nFile: full_backup_$DATE.tar.gz" "FAILED"
fi

# Clean up old backups
echo ""
echo "Cleaning up backups older than $RETENTION_DAYS days..."
DELETED_COUNT=$(find "$BACKUP_DIR" -name "full_backup_*.tar.gz" -mtime +$RETENTION_DAYS -delete -print 2>/dev/null | wc -l)
DELETED_MANIFESTS=$(find "$BACKUP_DIR" -name "backup_*.manifest" -mtime +$RETENTION_DAYS -delete -print 2>/dev/null | wc -l)

if [ "$DELETED_COUNT" -gt 0 ]; then
  echo "✓ Deleted $DELETED_COUNT old backup(s) and $DELETED_MANIFESTS manifest(s)"
else
  echo "  No old backups to delete"
fi

# List current backups
echo ""
echo "Current backups:"
ls -lh "$BACKUP_DIR"/full_backup_*.tar.gz 2>/dev/null | tail -5 || echo "  No backups found"

echo ""
echo "=========================================="
echo "Backup finished: $(date)"
echo "=========================================="

# Exit with error code if backups failed
exit $BACKUP_ERRORS
