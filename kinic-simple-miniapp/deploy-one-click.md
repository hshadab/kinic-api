# 🚀 One-Click Deployment Options

## Option 1: Deploy to Vercel (Easiest)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/kinic-base-miniapp)

**Steps:**
1. Click the button above
2. Connect your GitHub account
3. Import this project
4. Click "Deploy"
5. Get live URL in 2 minutes!

---

## Option 2: Deploy to Netlify

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/yourusername/kinic-base-miniapp)

**Steps:**
1. Click the button above
2. Connect GitHub
3. Auto-deploys your mini app
4. Get live URL instantly!

---

## Option 3: Manual Vercel CLI

```bash
cd kinic-simple-miniapp
npx vercel --prod
```

**Follow prompts:**
- Login to Vercel
- Confirm project settings
- Deploy automatically

---

## Option 4: Upload Build

```bash
# Build the app
npm run build

# Upload .next folder to any host:
# - Vercel.com (drag & drop)
# - Netlify.com (drag & drop)
# - Your own server
```