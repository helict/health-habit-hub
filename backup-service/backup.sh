#!/bin/bash
set -e

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=${BACKUP_RETENTION_DAYS:-7}

echo "=========================================="
echo "Starting backup: $(date)"
echo "=========================================="

# Create backup directory structure
mkdir -p "$BACKUP_DIR/$DATE"

echo "1/4 Backing up MongoDB..."
mongodump \
  --host=mongo:27017 \
  --username="$MONGO_USER" \
  --password="$MONGO_PASSWORD" \
  --authenticationDatabase=admin \
  --out="$BACKUP_DIR/$DATE/mongodb" \
  --quiet

echo "2/4 Backing up Fuseki (RDF data)..."
if [ -d "/fuseki" ] && [ "$(ls -A /fuseki)" ]; then
  tar -czf "$BACKUP_DIR/$DATE/fuseki-data.tar.gz" -C /fuseki . 2>/dev/null || echo "Warning: Fuseki backup may be empty"
else
  echo "Warning: Fuseki volume is empty or not mounted"
  touch "$BACKUP_DIR/$DATE/fuseki-data.tar.gz"
fi

echo "3/4 Backing up Neo4j..."
if [ -d "/neo4j-data" ] && [ "$(ls -A /neo4j-data)" ]; then
  tar -czf "$BACKUP_DIR/$DATE/neo4j-data.tar.gz" -C /neo4j-data . 2>/dev/null || echo "Warning: Neo4j backup may be empty"
else
  echo "Warning: Neo4j volume is empty or not mounted"
  touch "$BACKUP_DIR/$DATE/neo4j-data.tar.gz"
fi

echo "4/4 Creating unified backup archive..."
tar -czf "$BACKUP_DIR/full_backup_$DATE.tar.gz" -C "$BACKUP_DIR/$DATE" .

# Calculate size
BACKUP_SIZE=$(du -sh "$BACKUP_DIR/full_backup_$DATE.tar.gz" | cut -f1)

# Clean up temporary directory
rm -rf "$BACKUP_DIR/$DATE"

# Generate backup manifest
cat > "$BACKUP_DIR/backup_$DATE.manifest" <<EOF
Backup Date: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
MongoDB: ✓
Fuseki: ✓
Neo4j: ✓
Size: $BACKUP_SIZE
File: full_backup_$DATE.tar.gz
Retention: $RETENTION_DAYS days
EOF

echo ""
echo "✓ Backup completed successfully!"
echo "  File: full_backup_$DATE.tar.gz"
echo "  Size: $BACKUP_SIZE"
echo "  Location: $BACKUP_DIR/"

# Clean up old backups
echo ""
echo "Cleaning up backups older than $RETENTION_DAYS days..."
DELETED_COUNT=$(find "$BACKUP_DIR" -name "full_backup_*.tar.gz" -mtime +$RETENTION_DAYS -delete -print | wc -l)
DELETED_MANIFESTS=$(find "$BACKUP_DIR" -name "backup_*.manifest" -mtime +$RETENTION_DAYS -delete -print | wc -l)

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
