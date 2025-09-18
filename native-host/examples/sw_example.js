// Example MV3 service worker for Kinic native messaging integration.
// NOTE: Replace stubbed kinicStore/kinicRetrieve with your extension's real logic.

const HOST = 'com.kinic.api';
let port;

function connectNative() {
  if (port) return;
  try {
    port = chrome.runtime.connectNative(HOST);
  } catch (e) {
    console.error('connectNative failed:', e);
    return;
  }

  port.onMessage.addListener(handleNativeMessage);
  port.onDisconnect.addListener(() => {
    console.warn('Native host disconnected', chrome.runtime.lastError);
    port = undefined;
    setTimeout(connectNative, 1000);
  });
}

async function handleNativeMessage(msg) {
  const { id, action, params } = msg || {};
  let result, error;
  try {
    switch (action) {
      case 'kinic.store':
        result = await kinicStore(params || {});
        break;
      case 'kinic.retrieve':
        result = await kinicRetrieve(params || {});
        break;
      default:
        throw new Error('unknown_action');
    }
  } catch (e) {
    error = String(e && e.message ? e.message : e);
  }
  try { port?.postMessage({ id, ok: !error, result, error }); } catch {}
}

// Example: save active tab or provided URL/title/tags.
async function kinicStore(params) {
  const { url, title, tags, notes, content, selection, metadata, capture = true } = params;
  const { tab, targetUrl, targetTitle } = await resolveTarget(url, title);
  if (!targetUrl) throw new Error('no_url_available');

  let pageData = {};
  if (capture && (!content || !selection)) {
    // Prefer asking a declared content_script if available; otherwise use executeScript
    pageData = (await captureViaMessage(tab?.id)) || (await captureViaExecuteScript(tab?.id));
  }

  // TODO: Replace with your extension's real save logic
  // For example: persist to Kinic backend, then return an ID.
  return {
    saved: true,
    url: targetUrl,
    title: targetTitle || pageData.title || null,
    tags: Array.isArray(tags) ? tags : undefined,
    notes: notes || undefined,
    meta: metadata || undefined,
    selection: selection || pageData.selection || undefined,
    content: content || pageData.content || undefined,
    at: new Date().toISOString(),
  };
}

// Example: minimal retrieve; replace with your own implementation.
async function kinicRetrieve(params) {
  const { query, top_k = 5, filters } = params;
  if (!query) throw new Error('query_required');

  // TODO: Call your extension-side search against Kinic memory.
  // This stub returns dummy items to demonstrate structure.
  const items = Array.from({ length: Math.min(top_k, 5) }, (_, i) => ({
    id: `demo-${i + 1}`,
    title: `Result ${i + 1} for ${query}`,
    url: `https://example.com/${encodeURIComponent(query)}/${i + 1}`,
    score: 0.9 - i * 0.1,
    snippet: `Snippet for ${query} (#${i + 1})`,
    filters: filters || undefined,
  }));

  return { query, items };
}

async function resolveTarget(url, title) {
  let targetUrl = url;
  let targetTitle = title;
  let tab = null;

  if (!targetUrl || !targetTitle) {
    const tabs = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
    tab = tabs && tabs[0] ? tabs[0] : null;
    if (tab) {
      if (!targetUrl) targetUrl = tab.url;
      if (!targetTitle) targetTitle = tab.title;
    }
  }
  return { tab, targetUrl, targetTitle };
}

async function captureViaMessage(tabId) {
  if (!tabId) return null;
  try {
    const res = await chrome.tabs.sendMessage(tabId, { type: 'kinic.capture' });
    if (res && res.ok) return res;
  } catch (e) {
    // Likely no content script injected for this page
  }
  return null;
}

async function captureViaExecuteScript(tabId) {
  if (!tabId) return {};
  try {
    const [{ result }] = await chrome.scripting.executeScript({
      target: { tabId },
      func: () => {
        const selection = (window.getSelection && window.getSelection().toString()) || '';
        const title = document.title || null;
        const url = location.href;
        const text = (document.body && document.body.innerText) || '';
        const MAX = 200_000;
        const content = text.length > MAX ? text.slice(0, MAX) : text;
        return { ok: true, url, title, selection, content };
      },
      world: 'MAIN',
    });
    return result || {};
  } catch (e) {
    return {};
  }
}

chrome.runtime.onInstalled.addListener(connectNative);
chrome.runtime.onStartup.addListener(connectNative);
connectNative();
