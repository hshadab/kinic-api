# Kinic Base Integration

Enhanced desktop agent for Base mini app integration with the Kinic Chrome extension.

## Architecture

```
Base Mini App (hosted) → Kinic Base Agent (local) → PyAutoGUI → Kinic Chrome Extension → ICP
```

## Key Features

- **Enhanced CORS** - Works with hosted Base mini apps on Vercel, Netlify, etc.
- **WebSocket Support** - Real-time operation status updates
- **Better Error Handling** - Detailed error messages and suggestions
- **Status Monitoring** - Chrome browser and Kinic extension health checks
- **Operation Queue** - Handles multiple concurrent requests safely

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Use Existing Configuration**
   - Uses the same `kinic-config.json` from parent directory
   - If not found, uses default coordinates
   - Run coordinate setup scripts if needed

3. **Start the Agent**
   ```bash
   python kinic-base-agent.py
   ```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service status and configuration |
| `/api/status` | GET | Detailed system status |
| `/api/kinic/save` | POST | Save current page via Kinic extension |
| `/api/kinic/search-extract` | POST | Search with AI response extraction |

## WebSocket Events

- `connect` - Client connected
- `operation_status` - Real-time operation progress
- `operation_complete` - Operation finished (success/failure)

## Usage with Base Mini App

The Base mini app connects to `http://localhost:5007` for all operations:

```javascript
// Save page
await fetch('http://localhost:5007/api/kinic/save', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ url: window.location.href })
});

// Search memory
await fetch('http://localhost:5007/api/kinic/search-extract', {
  method: 'POST', 
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'your search query' })
});
```

## Differences from Original kinic-api.py

- **Port 5007** (vs 5006) - Avoids conflicts
- **Enhanced CORS** - Supports hosted deployments
- **WebSocket support** - Real-time updates
- **Better error handling** - More detailed responses
- **Status monitoring** - System health checks
- **Operation tracking** - Progress updates via WebSocket

## Development vs Production

### Development
- Base mini app: `http://localhost:3000`
- Desktop agent: `http://localhost:5007`

### Production  
- Base mini app: `https://your-app.vercel.app`
- Desktop agent: `http://localhost:5007` (user's machine)

## User Setup Instructions

1. Install Kinic Chrome extension
2. Download and run Kinic Base Agent
3. Access Base mini app from Base app or browser
4. Mini app automatically connects to local agent

## Troubleshooting

- **Chrome not detected**: Ensure Chrome browser is running
- **Kinic not accessible**: Run coordinate setup scripts
- **CORS errors**: Check allowed origins in agent configuration
- **WebSocket issues**: Verify port 5007 is not blocked