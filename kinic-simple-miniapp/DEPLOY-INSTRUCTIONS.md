# Deploy Your Kinic Base Mini App

## Quick Deployment via Bitbucket + Vercel (Recommended)

### Step 1: Create Bitbucket Repository
1. Go to [Bitbucket](https://bitbucket.org) and create new repository:
   - Name: `kinic-base-miniapp` 
   - Keep it private if preferred
   - Don't initialize with README (we have files already)

### Step 2: Push to Bitbucket
```bash
cd /home/hshadab/kinic/kinic-simple-miniapp
git push -u origin master
```

### Step 3: Deploy via Vercel
1. Go to [Vercel](https://vercel.com)
2. Click "New Project" 
3. **Select "Continue with Bitbucket"**
4. Import your `kinic-base-miniapp` repository
5. Vercel will auto-detect Next.js and deploy

**Much easier than CLI authentication!** ✅

## Your Mini App is Ready!

✅ **Built and tested locally**
✅ **Production optimized** 
✅ **CORS configured** for Base integration
✅ **Git repository initialized**

After deployment, you'll get a URL like: `https://kinic-ai-memory.vercel.app`

## What Happens Next

1. **Test the deployed app** - Visit the Vercel URL
2. **Start the desktop agent** - Run `python ../base-integration/kinic-base-agent.py` 
3. **Submit to Base** - Add your deployed URL to Base mini app directory

## Alternative Deployment Options

### Netlify
```bash
npm install -g netlify-cli
netlify login
netlify deploy --prod --dir=.next
```

### GitHub Pages (via actions)
Push to GitHub and enable Pages in repository settings.

## Troubleshooting

- If build fails: `npm run build` locally first
- If CORS issues: Check vercel.json configuration  
- If desktop agent connection fails: Ensure it's running on port 5007

**Your mini app is production-ready!** 🚀