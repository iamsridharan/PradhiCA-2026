#!/bin/bash
# PradhiCA - Deploy to pradhica.com
# Run from project root: ./deploy.sh
#
# IMPORTANT: macOS rsync copies local folder permissions (often 700).
# Hostinger Apache cannot read 700 directories → 403 Forbidden.
# We always fix remote permissions after rsync.

set -e

SSH_HOST="72.60.217.169"
SSH_PORT="65002"
SSH_USER="u925520622"
REMOTE_PATH="/home/u925520622/domains/pradhica.com/public_html"
LOCAL_PATH="$(cd "$(dirname "$0")" && pwd)"
SSH_OPTS=(-p "$SSH_PORT" -o BatchMode=yes)

echo "Deploying PradhiCA to pradhica.com..."
echo "Local:  $LOCAL_PATH"
echo "Remote: $SSH_USER@$SSH_HOST:$REMOTE_PATH (port $SSH_PORT)"
echo ""

rsync -avz --delete \
  -e "ssh -p $SSH_PORT" \
  --exclude '.git' \
  --exclude '.gitignore' \
  --exclude 'deploy.sh' \
  --exclude '*.zip' \
  --exclude 'node_modules' \
  --exclude '.DS_Store' \
  --exclude '.agents' \
  --exclude 'skills-lock.json' \
  "$LOCAL_PATH/" \
  "$SSH_USER@$SSH_HOST:$REMOTE_PATH/"

echo ""
echo "Fixing permissions on server (dirs 755, files 644)..."
ssh "${SSH_OPTS[@]}" "$SSH_USER@$SSH_HOST" \
  "find '$REMOTE_PATH' -type d -exec chmod 755 {} + && find '$REMOTE_PATH' -type f -exec chmod 644 {} +"

echo ""
echo "Deployment complete."
