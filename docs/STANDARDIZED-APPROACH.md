# Kinic API - Standardized Approach

## Core Principle
Every interaction with Kinic follows the exact same 5-step pattern to ensure consistency and prevent popup conflicts.

## The Standard Sequence

All endpoints (`/save`, `/search-and-retrieve`, `/search-ai-extract`) follow:

```
1. Focus Chrome         - Click at (500, 500) to ensure Chrome is active
2. Close existing popup - Press ESC (wait 2 seconds)
3. Open Kinic          - Click at configured position (2076, 144)
4. Perform action      - Endpoint-specific steps
5. Close Kinic         - Press ESC (wait 1 second)
```

## Endpoint-Specific Actions (Step 4)

### `/save`
- Press SHIFT+TAB to navigate to Save button
- Press ENTER to save
- Wait 3 seconds for save to complete

### `/search-and-retrieve`
- TAB 4 times to reach search field
- Type query and press ENTER
- Wait for results (4 seconds)
- TAB 2 times to first result
- SHIFT+F10 for context menu
- DOWN 5 times to "Copy link address"
- ENTER to copy URL

### `/search-ai-extract`
- TAB 4 times to reach search field
- Type query and press ENTER
- Wait for results (4 seconds)
- TAB 5 times to AI button
- ENTER to generate AI response
- Wait 10 seconds for generation
- Move to AI response area (1413, 1244)
- Triple-click to select text
- CTRL+C to copy
- Extract from clipboard

## Configuration

Coordinates are stored in `kinic-config.json`:
```json
{
    "kinic_x": 2076,
    "kinic_y": 144,
    "ai_response_x": 1413,
    "ai_response_y": 1244
}
```

## File Structure

```
kinic/
├── kinic-api.py              # Main API server (implements standard sequence)
├── kinic-config.json         # Coordinates configuration
├── capture-mouse-windows.py  # Capture Kinic button position
├── capture-ai-windows.py     # Capture AI response position
├── stripe-api-demo.py        # Multi-agent demo using the API
├── test-all-endpoints.py     # Test all three endpoints
├── README.md                 # User documentation
└── STANDARDIZED-APPROACH.md  # This file (technical reference)
```

## Running the System

1. **Setup coordinates** (one time):
   ```powershell
   python capture-mouse-windows.py
   python capture-ai-windows.py
   ```

2. **Start API server**:
   ```powershell
   python kinic-api.py
   ```

3. **Run demos/tests**:
   ```powershell
   python stripe-api-demo.py
   python test-all-endpoints.py
   ```

## Important Notes

- **Never** skip the Focus Chrome and ESC steps
- **Always** use the same timing between steps
- **All demos** call the API endpoints, so they automatically use this approach
- **No manual navigation** - the API handles everything
- **Console logging** shows each numbered step for debugging

## Why This Works

1. **Focus Chrome** ensures we're interacting with the right window
2. **Initial ESC** prevents duplicate popups
3. **Consistent timing** allows for page/UI loading
4. **Final ESC** ensures clean state for next action
5. **Numbered steps** in console make debugging easy

This approach is "hard-coded" into `kinic-api.py` and all demos use it automatically.