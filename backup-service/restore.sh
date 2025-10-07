#!/bin/bash
set -e

BACKUP_FILE=$1
RESTORE_DIR="/tmp/restore-$$"

if [ -z "$BACKUP_FILE" ]; then
  echo "Usage: docker-compose run backup /restore.sh <backup-file>"
  echo ""
  echo "Available backups:"
  ls -lh /backups/full_backup_*.tar.gz 2>/dev/null || echo "  No backups found"
  exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
  echo "Error: Backup file not found: $BACKUP_FILE"
  exit 1
fi

echo "=========================================="
echo "⚠️  WARNING: DATABASE RESTORE"
echo "=========================================="
echo "This will restore data from: $(basename $BACKUP_FILE)"
echo ""
echo "⚠️  This operation will:"
echo "  - OVERWRITE current MongoDB data"
echo "  - OVERWRITE current Fuseki data"
echo "  - OVERWRITE current Neo4j data"
echo ""
read -p "Type 'YES' to continue: " confirm

if [ "$confirm" != "YES" ]; then
  echo "Restore cancelled"
  exit 0
fi

echo ""
echo "Starting restore from: $BACKUP_FILE"

# Extract backup
mkdir -p "$RESTORE_DIR"
echo "Extracting backup archive..."
tar -xzf "$BACKUP_FILE" -C "$RESTORE_DIR"

# Restore MongoDB
echo ""
echo "1/3 Restoring MongoDB..."
if [ -d "$RESTORE_DIR/mongodb" ]; then
  mongorestore \
    --host=mongo:27017 \
    --username="$MONGO_USER" \
    --password="$MONGO_PASSWORD" \
    --authenticationDatabase=admin \
    --drop \
    "$RESTORE_DIR/mongodb" \
    --quiet
  echo "✓ MongoDB restored"
else
  echo "Warning: No MongoDB backup found in archive"
fi

# Restore Fuseki
echo ""
echo "2/3 Restoring Fuseki..."
if [ -f "$RESTORE_DIR/fuseki-data.tar.gz" ] && [ -s "$RESTORE_DIR/fuseki-data.tar.gz" ]; then
  rm -rf /fuseki/*
  tar -xzf "$RESTORE_DIR/fuseki-data.tar.gz" -C /fuseki/
  echo "✓ Fuseki restored"
else
  echo "Warning: No Fuseki backup found in archive"
fi

# Restore Neo4j
echo ""
echo "3/3 Restoring Neo4j..."
if [ -f "$RESTORE_DIR/neo4j-data.tar.gz" ] && [ -s "$RESTORE_DIR/neo4j-data.tar.gz" ]; then
  echo "Note: Neo4j must be stopped before restore. Please stop the neo4j container manually."
  echo "Then extract: tar -xzf $RESTORE_DIR/neo4j-data.tar.gz -C /neo4j-data/"
  echo "✓ Neo4j backup ready (manual restore required)"
else
  echo "Warning: No Neo4j backup found in archive"
fi

# Cleanup
rm -rf "$RESTORE_DIR"

echo ""
echo "=========================================="
echo "✓ Restore completed!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Restart services: docker-compose restart"
echo "  2. Verify data integrity"
