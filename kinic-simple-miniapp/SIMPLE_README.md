# Kinic Simple Base Mini App

A clean, minimal Base mini app for Kinic AI memory integration.

## Key Features

✅ **No Farcaster dependency** - Works as standalone Base mini app  
✅ **Simple Next.js setup** - Minimal dependencies  
✅ **Desktop agent integration** - Connects to local Kinic Base Agent  
✅ **Real-time status** - Shows connection to desktop agent  
✅ **Clean UI** - Focus on Kinic memory functionality  

## Architecture

```
Simple Base Mini App → Desktop Agent (localhost:5007) → Chrome Extension → ICP
```

## What's Different

This is a **simplified version** compared to the complex MiniKit version:

- ❌ **No Farcaster authentication** - Pure Base mini app
- ❌ **No complex MiniKit SDK** - Just Next.js + Tailwind
- ❌ **No environment dependencies** - Minimal setup
- ✅ **Cleaner codebase** - Easier to understand and modify
- ✅ **Same functionality** - Full Kinic memory integration

## Usage

### Development
```bash
npm run dev
```

### Production Build
```bash
npm run build
npm start
```

### With Desktop Agent
1. Start the desktop agent: 
   ```bash
   cd ../base-integration
   source venv/bin/activate
   python kinic-base-agent.py
   ```

2. Access mini app at `http://localhost:3000`

3. Use save/search functionality with real Chrome extension automation

## Deployment

This can be deployed to any hosting platform:
- Vercel
- Netlify  
- Heroku
- Any static hosting

The desktop agent runs locally on each user's machine.

## Mini App Distribution

As a Base mini app, this can be:
- Listed in Base mini app directory
- Shared via social media
- Discovered in Base app feed
- Accessed via direct URL

## Dependencies

Minimal dependencies:
- Next.js 15
- React 19
- Tailwind CSS
- TypeScript

No complex blockchain or Farcaster dependencies needed.