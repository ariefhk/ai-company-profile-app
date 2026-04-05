#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/venv/bin/activate"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log()    { echo -e "${BLUE}[seed]${NC} $1"; }
success(){ echo -e "${GREEN}[✔]${NC} $1"; }
error()  { echo -e "${RED}[✘]${NC} $1"; exit 1; }

usage() {
  echo ""
  echo "Usage: ./seed.sh [seeder_name]"
  echo ""
  echo "  ./seed.sh              Run all seeders in seeds/"
  echo "  ./seed.sh user         Run seeds/user_seeder.py"
  echo "  ./seed.sh category     Run seeds/category_seeder.py"
  echo ""
  echo "Available seeders:"
  for f in seeds/*_seeder.py; do
    [ -f "$f" ] || continue
    name=$(basename "$f" _seeder.py)
    echo "  $name"
  done
  echo ""
}

if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
  usage
  exit 0
fi

if [ -n "$1" ]; then
  log "Running seeder: $1"
  python -c "
import asyncio
from core.database import AsyncSessionLocal
from seeds.${1}_seeder import run

async def main():
    async with AsyncSessionLocal() as db:
        try:
            await run(db)
            await db.commit()
            print('\033[0;32m[✔]\033[0m Seeded: ${1}')
        except Exception as e:
            await db.rollback()
            print(f'\033[0;31m[✘]\033[0m ${1}: {e}')
            exit(1)

asyncio.run(main())
"
else
  log "Running all seeders..."
  python -c "
import asyncio
import glob
import importlib
import os

from core.database import AsyncSessionLocal

async def main():
    async with AsyncSessionLocal() as db:
        files = sorted(glob.glob('seeds/*_seeder.py'))
        try:
            for f in files:
                name = os.path.basename(f).removesuffix('.py')
                mod = importlib.import_module(f'seeds.{name}')
                await mod.run(db)
                print(f'\033[0;32m[✔]\033[0m Seeded: {name.removesuffix(\"_seeder\")}')
            await db.commit()
        except Exception as e:
            await db.rollback()
            print(f'\033[0;31m[✘]\033[0m {e}')
            exit(1)

asyncio.run(main())
"
fi
