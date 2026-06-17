#!/bin/bash
# PradhiCA - Deploy to pradhica.com
# Run from project root: ./deploy.sh

set -e

# SSH config (password NOT stored - use SSH key or enter when prompted)
SSH_HOST="72.60.217.169"
SSH_PORT="65002"
SSH_USER="u925520622"
REMOTE_PATH="/home/u925520622/domains/pradhica.com/public_html"
LOCAL_PATH="$(cd "$(dirname "$0")" && pwd)"

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
  "$LOCAL_PATH/" \
  "$SSH_USER@$SSH_HOST:$REMOTE_PATH/"

echo ""
echo "Deployment complete."
