#!/bin/bash
# PradhiCA - Deploy to pradhica.com
#
# Usage:
#   ./deploy.sh                  # full sync (fast excludes, no --delete)
#   ./deploy.sh --delete         # full sync + remove remote orphans
#   ./deploy.sh file1.html ...   # partial: only listed files/folders
#   ./deploy.sh --delete f.html  # partial with --delete is ignored (safe)
#
# IMPORTANT: macOS rsync can copy local dir perms as 700.
# Hostinger Apache cannot read 700 dirs → 403. We only fix bad dirs.

set -e

# Uses ~/.ssh/config Host "aspire-hostinger" (IdentityFile hostinger_aspire).
# Do NOT connect by raw IP — that skips the Hostinger key and auth fails.
SSH_ALIAS="aspire-hostinger"
REMOTE_PATH="/home/u925520622/domains/pradhica.com/public_html"
LOCAL_PATH="$(cd "$(dirname "$0")" && pwd)"
SSH_OPTS=(-o BatchMode=yes)
RSYNC_SSH="ssh"

DO_DELETE=0
FILES=()

for arg in "$@"; do
  case "$arg" in
    --delete) DO_DELETE=1 ;;
    -h|--help)
      sed -n '2,12p' "$0"
      exit 0
      ;;
    *) FILES+=("$arg") ;;
  esac
done

RSYNC_EXCLUDES=(
  --exclude '.git/'
  --exclude '.gitignore'
  --exclude '.env'
  --exclude '.env.*'
  --exclude '.DS_Store'
  --exclude '.cursor/'
  --exclude '.agents/'
  --exclude 'node_modules/'
  --exclude 'deploy.sh'
  --exclude 'ftp_sync.py'
  --exclude 'manual_ftp_sync.py'
  --exclude 'watch_and_sync.py'
  --exclude 'update_headers_footers.py'
  --exclude 'package.json'
  --exclude 'package-lock.json'
  --exclude 'skills-lock.json'
  --exclude 'scripts/'
  --exclude 'OldBCK/'
  --exclude 'Schedules_2025/'
  --exclude '*.zip'
  --exclude '*.md'
  --exclude '__pycache__/'
  --exclude '*.pyc'
  --exclude 'error_log'
  --exclude '*-scrap.html'
)

fix_remote_perms() {
  echo ""
  echo "Fixing locked dirs (700 → 755) if any..."
  ssh "${SSH_OPTS[@]}" "$SSH_ALIAS" \
    "find '$REMOTE_PATH' -type d -perm 700 -exec chmod 755 {} + 2>/dev/null || true"
}

echo "Deploying PradhiCA to pradhica.com..."
echo "Local:  $LOCAL_PATH"
echo "Remote: $SSH_ALIAS:$REMOTE_PATH"
echo ""

if [ ${#FILES[@]} -gt 0 ]; then
  # --- Partial deploy ---
  echo "Mode: PARTIAL (${#FILES[@]} path(s))"
  MISSING=0
  for f in "${FILES[@]}"; do
    if [ ! -e "$LOCAL_PATH/$f" ] && [ ! -e "$f" ]; then
      echo "ERROR: not found: $f"
      MISSING=1
    fi
  done
  [ "$MISSING" -eq 0 ] || exit 1

  # Resolve paths relative to project root for rsync
  REL_FILES=()
  for f in "${FILES[@]}"; do
    if [ -e "$LOCAL_PATH/$f" ]; then
      REL_FILES+=("$f")
    else
      # absolute or cwd-relative path → make relative to LOCAL_PATH
      REL_FILES+=("$(python3 -c "import os,sys; print(os.path.relpath(sys.argv[1], sys.argv[2]))" "$(cd "$(dirname "$f")" && pwd)/$(basename "$f")" "$LOCAL_PATH")")
    fi
  done

  # Upload each path; preserve relative structure under public_html
  for f in "${REL_FILES[@]}"; do
    src="$LOCAL_PATH/$f"
    if [ -d "$src" ]; then
      echo "→ dir  $f/"
      rsync -avz \
        -e "$RSYNC_SSH" \
        "${RSYNC_EXCLUDES[@]}" \
        "$src/" \
        "$SSH_ALIAS:$REMOTE_PATH/$f/"
    else
      remote_dir=$(dirname "$f")
      echo "→ file $f"
      if [ "$remote_dir" = "." ]; then
        rsync -avz -e "$RSYNC_SSH" "$src" "$SSH_ALIAS:$REMOTE_PATH/"
      else
        ssh "${SSH_OPTS[@]}" "$SSH_ALIAS" "mkdir -p '$REMOTE_PATH/$remote_dir'"
        rsync -avz -e "$RSYNC_SSH" "$src" "$SSH_ALIAS:$REMOTE_PATH/$remote_dir/"
      fi
    fi
  done
else
  # --- Full deploy ---
  echo "Mode: FULL$([ "$DO_DELETE" -eq 1 ] && echo ' (--delete)' || echo ' (additive)')"
  RSYNC_OPTS=(-avz)
  [ "$DO_DELETE" -eq 1 ] && RSYNC_OPTS+=(--delete)

  rsync "${RSYNC_OPTS[@]}" \
    -e "$RSYNC_SSH" \
    "${RSYNC_EXCLUDES[@]}" \
    "$LOCAL_PATH/" \
    "$SSH_ALIAS:$REMOTE_PATH/"
fi

fix_remote_perms

echo ""
echo "Deployment complete."
