# Kinic Base Mini App - User Setup Guide

Complete guide for users to set up the Kinic Base mini app with desktop agent integration.

## 🎯 What You're Setting Up

```
Base Mini App (your phone/browser) → Desktop Agent (your computer) → Chrome Extension → ICP Memory
```

## 📋 Prerequisites

1. **Kinic Chrome Extension** - Install from Chrome Web Store
2. **Chrome Browser** - Must be running on your desktop
3. **Python 3** - For the desktop agent
4. **Base App or Browser** - To access the mini app

## 🖥️ Desktop Setup (Required)

### Step 1: Download the Code
```bash
git clone https://your-repo/kinic-base-integration
cd kinic-base-integration
```

### Step 2: Run Setup
```bash
./setup.sh
```

### Step 3: Start Desktop Agent
```bash
source venv/bin/activate
python kinic-base-agent.py
```

You should see:
```
🚀 Kinic Base Agent
✅ WebSocket support for real-time updates
📱 Ready for Base mini app connections
🌐 Running on http://localhost:5007
```

### Step 4: Verify Chrome Integration
Open another terminal and test:
```bash
curl http://localhost:5007/api/status
```

Should return:
```json
{
  "agent": "running",
  "chrome_browser": true,
  "ready": true,
  "message": "Ready for operations"
}
```

## 📱 Base Mini App Access

### Option 1: Via Base App (Recommended)
1. Open Base app on your phone
2. Look for "Kinic AI Memory" in feed or search
3. Tap "Launch Kinic"
4. Sign in with Farcaster

### Option 2: Via Browser
1. Go to the hosted mini app URL
2. Sign in with Farcaster
3. Use save/search functionality

## 🔧 Troubleshooting

### "Chrome browser not detected"
- Ensure Chrome is running on your desktop
- The desktop agent needs Chrome to be open

### "Kinic extension not accessible"
- Install Kinic Chrome extension
- Run coordinate setup if needed:
  ```bash
  cd ../setup-tools
  python capture-mouse-windows.py  # Set Kinic button
  python capture-ai-windows.py     # Set AI response area
  ```

### "Connection refused" from Base mini app
- Ensure desktop agent is running on localhost:5007
- Check firewall settings
- Verify CORS origins include your mini app domain

### Coordinate issues
- Each user needs to calibrate coordinates for their screen
- Use the setup tools in the parent directory
- Coordinates are saved in `kinic-config.json`

## 🎮 How to Use

### Save a Page
1. Navigate to any webpage in Chrome
2. In Base mini app, click "Save Current Page"
3. Watch the desktop agent automatically:
   - Click Kinic extension
   - Navigate to save button
   - Save the page
   - Close extension

### Search Your Memory
1. In Base mini app, type your search query
2. Click "Search"
3. Watch the desktop agent automatically:
   - Open Kinic extension
   - Type your query
   - Click AI button
   - Extract AI response
   - Return results to mini app

## 🚀 Production Deployment

### For Mini App Developers
1. Deploy Base mini app to Vercel/Netlify
2. Update CORS origins in desktop agent
3. Provide setup instructions to users

### For End Users
1. Install desktop agent (one-time setup)
2. Keep it running when using Base mini app
3. Enjoy seamless AI memory integration

## 🔒 Security Notes

- Desktop agent only runs locally
- No data passes through external servers
- All communication secured via localhost
- Chrome extension maintains ICP connection

## 📞 Support

If you need help:
1. Check the troubleshooting section
2. Verify all prerequisites are met
3. Test with curl commands
4. Check desktop agent logs for errors