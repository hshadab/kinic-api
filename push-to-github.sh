#!/bin/bash

echo "🚀 Setting up Git repository and pushing to GitHub..."

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Kinic Desktop app with multi-platform support

- Desktop GUI application for easy setup
- No more coordinate typing required
- System tray support
- Multi-platform builds via GitHub Actions
- Updated documentation with download links"

# Add your GitHub repository as remote
echo ""
echo "📋 Next steps:"
echo "1. Create a new repository on GitHub named 'kinic-api'"
echo "2. Run these commands:"
echo ""
echo "git remote add origin https://github.com/YOUR_USERNAME/kinic-api.git"
echo "git branch -M main"
echo "git push -u origin main"
echo ""
echo "3. Create a release to trigger builds:"
echo "git tag v1.0.0"
echo "git push origin v1.0.0"
echo ""
echo "Replace YOUR_USERNAME with your GitHub username!"