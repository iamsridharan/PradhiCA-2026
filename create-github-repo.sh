#!/bin/bash

# Script to create GitHub repository and push code
# Usage: ./create-github-repo.sh

REPO_NAME="PradhiCA-2026"
REPO_DESCRIPTION="Premier CA Test Series Platform for Foundation, Intermediate & Final Coaching"

echo "🚀 Creating GitHub repository: $REPO_NAME"
echo ""

# Check if GitHub CLI is installed
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI found. Creating repository..."
    gh repo create "$REPO_NAME" --public --description "$REPO_DESCRIPTION" --source=. --remote=origin --push
    echo "✅ Repository created and code pushed!"
else
    echo "⚠️  GitHub CLI not found."
    echo ""
    echo "Please choose one of the following options:"
    echo ""
    echo "Option 1: Install GitHub CLI (recommended)"
    echo "  brew install gh"
    echo "  gh auth login"
    echo "  Then run this script again"
    echo ""
    echo "Option 2: Create repository manually"
    echo "  1. Go to https://github.com/new"
    echo "  2. Repository name: $REPO_NAME"
    echo "  3. Description: $REPO_DESCRIPTION"
    echo "  4. Choose Public or Private"
    echo "  5. DO NOT initialize with README, .gitignore, or license"
    echo "  6. Click 'Create repository'"
    echo "  7. Then run these commands:"
    echo "     git remote add origin https://github.com/YOUR_USERNAME/$REPO_NAME.git"
    echo "     git branch -M main"
    echo "     git push -u origin main"
    echo ""
fi
