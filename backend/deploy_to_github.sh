#!/bin/bash

echo "🚀 Deploying Beya Tech Backend to GitHub..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
fi

# Add all files
echo "📁 Adding files to git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Initial commit: Django REST API for Beya Tech e-commerce platform

Features:
- User authentication (register/login)
- Product management with categories
- JWT token authentication
- Comprehensive API endpoints
- Unit tests and manual testing tools
- Proper error handling and validation"

# Check if remote origin exists
if git remote get-url origin >/dev/null 2>&1; then
    echo "🔗 Remote origin already exists"
else
    echo "🔗 Adding remote origin..."
    echo "Please enter your GitHub repository URL (e.g., https://github.com/username/beya-tech-backend.git):"
    read repo_url
    git remote add origin $repo_url
fi

# Push to GitHub
echo "⬆️ Pushing to GitHub..."
git branch -M main
git push -u origin main

echo "✅ Successfully deployed to GitHub!"
echo "🌐 Your repository is now available at: $(git remote get-url origin)"
