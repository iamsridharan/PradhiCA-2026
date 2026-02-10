# GitHub Repository Setup Guide

## Step 1: Authenticate with GitHub CLI

Run the following command and follow the prompts:

```bash
gh auth login
```

Choose:
- **GitHub.com** (default)
- **HTTPS** (recommended)
- **Login with a web browser** (easiest)

## Step 2: Create the Repository

Once authenticated, run:

```bash
gh repo create "PradhiCA-2026" --public --description "Premier CA Test Series Platform for Foundation, Intermediate & Final Coaching" --source=. --remote=origin --push
```

This will:
- Create a public repository named "PradhiCA-2026" on GitHub
- Add it as the remote origin
- Push your code to the main branch

## Alternative: Manual Creation

If you prefer to create it manually:

1. Go to https://github.com/new
2. Repository name: `PradhiCA-2026`
3. Description: `Premier CA Test Series Platform for Foundation, Intermediate & Final Coaching`
4. Choose **Public** or **Private**
5. **DO NOT** check "Initialize this repository with a README"
6. Click **Create repository**
7. Then run these commands:

```bash
git remote add origin https://github.com/YOUR_USERNAME/PradhiCA-2026.git
git branch -M main
git push -u origin main
```

## Current Status

✅ Git repository initialized  
✅ README.md created  
✅ .gitignore created  
✅ Initial commit made  
⏳ Waiting for GitHub authentication and repository creation
