#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log()    { echo -e "${BLUE}[migrate]${NC} $1"; }
success(){ echo -e "${GREEN}[✔]${NC} $1"; }
warn()   { echo -e "${YELLOW}[!]${NC} $1"; }
error()  { echo -e "${RED}[✘]${NC} $1"; exit 1; }

usage() {
  echo ""
  echo "Usage: ./migrate.sh [command] [options]"
  echo ""
  echo "  generate <message>   Autogenerate a new migration"
  echo "  upgrade              Apply all pending migrations"
  echo "  downgrade            Roll back the last migration"
  echo "  downgrade <rev>      Roll back to a specific revision"
  echo "  status               Show current migration state"
  echo "  history              Show full migration history"
  echo "  reset                Downgrade to base (wipes all tables)"
  echo "  fresh                Reset + upgrade head (clean slate)"
  echo ""
}

check_alembic() {
  command -v alembic &>/dev/null || error "alembic not found. Is your venv activated?"
}

check_versions_dir() {
  [ -d "alembic/versions" ] || error "alembic/versions not found. Are you in the project root?"
}

review_latest_migration() {
  latest=$(ls -t alembic/versions/*.py 2>/dev/null | head -1)
  if [ -n "$latest" ]; then
    warn "Review the generated migration before applying:"
    echo -e "  ${YELLOW}cat $latest${NC}"
    echo ""
  fi
}

case "$1" in

  generate)
    [ -z "$2" ] && error "Please provide a message. Example: ./migrate.sh generate 'add users table'"
    check_alembic
    check_versions_dir
    log "Generating migration: '$2'"
    alembic revision --autogenerate -m "$2"
    echo ""
    success "Migration file created in alembic/versions/"
    review_latest_migration
    warn "Run './migrate.sh upgrade' when ready to apply."
    ;;

  upgrade)
    check_alembic
    log "Applying all pending migrations..."
    alembic upgrade head
    echo ""
    success "Database is up to date."
    ;;

  downgrade)
    check_alembic
    target="${2:--1}"
    warn "Rolling back to: $target"
    read -p "Are you sure? (y/N): " confirm
    [[ "$confirm" =~ ^[Yy]$ ]] || { log "Cancelled."; exit 0; }
    alembic downgrade "$target"
    echo ""
    success "Downgrade complete."
    ;;

  status)
    check_alembic
    log "Current migration status:"
    echo ""
    alembic current
    echo ""
    log "Pending migrations:"
    alembic heads
    ;;

  history)
    check_alembic
    log "Migration history:"
    echo ""
    alembic history --verbose
    ;;

  reset)
    check_alembic
    error_msg="This will downgrade ALL migrations (drop all tables)."
    warn "$error_msg"
    read -p "Type 'yes' to confirm: " confirm
    [ "$confirm" = "yes" ] || { log "Cancelled."; exit 0; }
    log "Downgrading to base..."
    alembic downgrade base
    echo ""
    success "All migrations rolled back."
    ;;

  fresh)
    check_alembic
    warn "This will RESET the database and re-apply all migrations."
    read -p "Type 'yes' to confirm: " confirm
    [ "$confirm" = "yes" ] || { log "Cancelled."; exit 0; }
    log "Downgrading to base..."
    alembic downgrade base
    log "Upgrading to head..."
    alembic upgrade head
    echo ""
    success "Fresh migration complete."
    ;;

  *)
    usage
    ;;
esac