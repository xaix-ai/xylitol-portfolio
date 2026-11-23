#!/usr/bin/env bash
# Copies every table (schema + data) from the Aiven database to Neon.
#
# Your portfolio tables are `managed = False`, so Django's `migrate` can't
# recreate them. This copies them as they are, together with Django's own
# tables (admin users, sessions, migration history).
#
# Usage:
#   export AIVEN_URL='postgres://avnadmin:PASSWORD@HOST:PORT/defaultdb?sslmode=require'
#   export NEON_URL='postgresql://USER:PASSWORD@ep-xxxx.REGION.aws.neon.tech/neondb?sslmode=require'
#   bash scripts/copy_aiven_to_neon.sh
#
# Needs pg_dump / pg_restore / psql at least as new as Aiven's Postgres
# version (check with: psql "$AIVEN_URL" -c 'select version()').

set -euo pipefail

: "${AIVEN_URL:?Set AIVEN_URL to your Aiven connection string}"
: "${NEON_URL:?Set NEON_URL to your Neon connection string}"

DUMP_FILE="aiven_backup_$(date +%Y%m%d_%H%M%S).dump"

echo "1/4  Checking both databases are reachable..."
psql "$AIVEN_URL" -Atc 'select version()'
psql "$NEON_URL"  -Atc 'select version()'

echo "2/4  Dumping Aiven (public schema) to $DUMP_FILE ..."
# --no-owner / --no-acl: Aiven's 'avnadmin' role doesn't exist on Neon,
# so ownership and grants are dropped and everything belongs to your Neon user.
pg_dump "$AIVEN_URL" \
  --format=custom \
  --schema=public \
  --no-owner \
  --no-acl \
  --file="$DUMP_FILE"

echo "3/4  Restoring into Neon..."
# Neon already has a "public" schema, so skip the CREATE SCHEMA entry
# and restore everything else.
TOC_FILE="$(mktemp)"
pg_restore --list "$DUMP_FILE" | grep -v ' SCHEMA - public ' > "$TOC_FILE"
pg_restore \
  --dbname="$NEON_URL" \
  --use-list="$TOC_FILE" \
  --no-owner \
  --no-acl \
  --single-transaction \
  --exit-on-error \
  "$DUMP_FILE"
rm -f "$TOC_FILE"

echo "4/4  Row counts on Neon:"
psql "$NEON_URL" -c "
select relname as table, n_live_tup as rows
from pg_stat_user_tables
order by relname;"

echo
echo "Done. Keep $DUMP_FILE as a backup (it's in .gitignore)."
