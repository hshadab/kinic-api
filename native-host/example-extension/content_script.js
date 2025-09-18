// Minimal content script matching examples/content_script.js

chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
  if (msg && msg.type === 'kinic.capture') {
    try {
      const selection = (window.getSelection && window.getSelection().toString()) || '';
      const title = document.title || null;
      const url = location.href;
      const text = (document.body && document.body.innerText) || '';
      const MAX = 200_000;
      const content = text.length > MAX ? text.slice(0, MAX) : text;
      sendResponse({ ok: true, url, title, selection, content });
    } catch (e) {
      sendResponse({ ok: false, error: String(e) });
    }
    return true; // async response
  }
});

