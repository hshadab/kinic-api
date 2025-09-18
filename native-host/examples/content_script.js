// Minimal content script for capturing page data
// Include in manifest.json under "content_scripts" with matches you need.

chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
  if (msg && msg.type === 'kinic.capture') {
    try {
      const selection = (window.getSelection && window.getSelection().toString()) || '';
      const title = document.title || null;
      const url = location.href;
      // Use innerText for readable text; may be large on long pages
      const text = (document.body && document.body.innerText) || '';
      // Keep payload reasonable
      const MAX = 200_000; // ~200k chars
      const content = text.length > MAX ? text.slice(0, MAX) : text;

      sendResponse({ ok: true, url, title, selection, content });
    } catch (e) {
      sendResponse({ ok: false, error: String(e) });
    }
    return true; // async response
  }
});

