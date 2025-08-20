# Kinic Base Mini App

A Base blockchain mini app that provides a frontend interface for the Kinic AI memory system via UI automation.

## Architecture

**The Kinic API is NOT on ICP - it's a UI automation wrapper that controls the Chrome extension!**

```
Base Mini App → Kinic API (localhost:5006) → PyAutoGUI → Kinic Chrome Extension → ICP Backend
```

- **Frontend**: Next.js + OnchainKit on Base blockchain (this app)
- **Automation Layer**: Kinic API (Flask + PyAutoGUI for UI automation)
- **UI Layer**: Kinic Chrome Extension (actual interface to ICP)
- **Backend**: ICP with semantic vector database

## Features

- 🔗 **Base Wallet Integration**: Connect with any Base-compatible wallet
- 🧠 **AI Memory Operations**: Save and search knowledge with semantic understanding
- 🔍 **Intelligent Search**: AI-powered query responses from saved content
- ⛓️ **Cross-Chain**: Base frontend + ICP backend integration
- 🎨 **Modern UI**: Responsive design with Tailwind CSS

## Setup

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Configure Environment**
   Copy `.env.local` and add your OnchainKit API key:
   ```env
   NEXT_PUBLIC_ONCHAINKIT_API_KEY=your_key_here
   ```

3. **Start Kinic API** (Required)
   Make sure the Kinic API is running on `localhost:5006`:
   ```bash
   # In the parent directory
   python kinic-api.py
   ```

4. **Run the App**
   ```bash
   npm run dev
   ```

## Usage

1. **Connect Wallet**: Use the wallet button to connect to Base
2. **Save Pages**: Click "Save Current Page" to store the current browser page to Kinic memory
3. **Search Memory**: Query your saved knowledge with natural language
4. **View Results**: See AI-generated responses based on your saved content

## API Integration

The app connects to the Kinic API (UI automation wrapper):

**How it works:**
1. **`/save`** - Automates Chrome extension to save current page:
   - PyAutoGUI clicks Kinic button
   - Navigates to save button (SHIFT+TAB)
   - Presses Enter to save

2. **`/search-ai-extract`** - Automates search with AI extraction:
   - Opens Kinic extension
   - Types search query
   - Clicks AI button
   - Extracts AI response text via clipboard

**Requirements:**
- Kinic Chrome extension installed and configured
- Kinic API running on localhost:5006
- Proper coordinate calibration for your screen

## Base Mini App Features

- OnchainKit integration for wallet connectivity
- Base blockchain compatibility
- Modern responsive UI
- Real-time memory operations
- Cross-chain data flow (Base ↔ ICP)

## Development

Built with:
- Next.js 15 + TypeScript
- OnchainKit for Base integration
- Tailwind CSS for styling
- Kinic API for memory operations