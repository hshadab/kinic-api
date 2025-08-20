'use client';

import { useState, useEffect } from 'react';
import { Avatar, Name, Badge, Identity, EthBalance } from '@coinbase/onchainkit/identity';
import { ConnectWallet, Wallet, WalletDropdown, WalletDropdownLink, WalletDropdownDisconnect } from '@coinbase/onchainkit/wallet';

interface Memory {
  id: number;
  query: string;
  response: string;
  timestamp: string;
}

export default function Home() {
  const [searchQuery, setSearchQuery] = useState('');
  const [memories, setMemories] = useState<Memory[]>([]);
  const [loading, setLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState<'checking' | 'connected' | 'disconnected'>('checking');

  useEffect(() => {
    const checkApiStatus = async () => {
      try {
        const response = await fetch('http://localhost:5006/');
        if (response.ok) {
          setApiStatus('connected');
        } else {
          setApiStatus('disconnected');
        }
      } catch (error) {
        setApiStatus('disconnected');
      }
    };

    checkApiStatus();
    const interval = setInterval(checkApiStatus, 10000); // Check every 10 seconds
    return () => clearInterval(interval);
  }, []);

  const handleSavePage = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5006/save', {
        method: 'POST',
      });
      const result = await response.json();
      if (result.success) {
        alert('Page saved to Kinic memory!');
      } else {
        alert('Failed to save page: ' + result.error);
      }
    } catch (error) {
      alert('Error connecting to Kinic API: ' + error);
    }
    setLoading(false);
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5006/search-ai-extract', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: searchQuery }),
      });
      const result = await response.json();
      if (result.success) {
        setMemories(prev => [...prev, {
          id: Date.now(),
          query: searchQuery,
          response: result.ai_response,
          timestamp: new Date().toLocaleString()
        }]);
        setSearchQuery('');
      } else {
        alert('Search failed: ' + result.error);
      }
    } catch (error) {
      alert('Error connecting to Kinic API: ' + error);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <header className="p-6 border-b border-gray-200 dark:border-gray-700 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
              Kinic
            </h1>
            <span className="px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full text-sm font-medium">
              AI Memory on Base
            </span>
          </div>
          
          <Wallet>
            <ConnectWallet>
              <Avatar className="h-6 w-6" />
              <Name />
            </ConnectWallet>
            <WalletDropdown>
              <Identity className="px-4 pt-3 pb-2" hasCopyAddressOnClick>
                <Avatar />
                <Name />
                <Badge />
                <EthBalance />
              </Identity>
              <WalletDropdownLink icon="wallet" href="https://keys.coinbase.com">
                Wallet
              </WalletDropdownLink>
              <WalletDropdownDisconnect />
            </WalletDropdown>
          </Wallet>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          {/* Left Panel - Memory Operations */}
          <div className="space-y-6">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
              <h2 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">Memory Operations</h2>
              
              {/* Save Current Page */}
              <div className="mb-6">
                <h3 className="text-lg font-semibold mb-2 text-gray-700 dark:text-gray-300">Save Current Page</h3>
                <p className="text-gray-600 dark:text-gray-400 text-sm mb-3">
                  Automate Kinic Chrome extension to save the current browser page to ICP memory
                </p>
                <div className="mb-2 p-2 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded text-xs text-yellow-800 dark:text-yellow-200">
                  ⚠️ Requires: Kinic Chrome extension installed + Kinic API running (localhost:5006)
                </div>
                <button
                  onClick={handleSavePage}
                  disabled={loading}
                  className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white font-medium py-3 px-4 rounded-lg transition-colors"
                >
                  {loading ? 'Automating Chrome Extension...' : 'Save Current Page'}
                </button>
              </div>

              {/* Search Memory */}
              <div>
                <h3 className="text-lg font-semibold mb-2 text-gray-700 dark:text-gray-300">Search Memory</h3>
                <p className="text-gray-600 dark:text-gray-400 text-sm mb-3">
                  Automate Kinic extension to query saved knowledge with AI-powered semantic search
                </p>
                <div className="mb-2 p-2 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded text-xs text-blue-800 dark:text-blue-200">
                  🤖 UI Automation: Opens extension → Types query → Clicks AI button → Extracts response
                </div>
                <div className="flex space-x-2">
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Ask about your saved knowledge..."
                    className="flex-1 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                    onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                  />
                  <button
                    onClick={handleSearch}
                    disabled={loading || !searchQuery.trim()}
                    className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white font-medium py-3 px-6 rounded-lg transition-colors"
                  >
                    {loading ? 'Automating...' : 'Search'}
                  </button>
                </div>
              </div>
            </div>

            {/* Architecture */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
              <h3 className="text-lg font-semibold mb-4 text-gray-800 dark:text-white">Architecture</h3>
              <ul className="space-y-3 text-gray-600 dark:text-gray-400">
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-blue-500 rounded-full mr-3"></span>
                  Base blockchain frontend (this app)
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-green-500 rounded-full mr-3"></span>
                  Kinic API (UI automation wrapper)
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-orange-500 rounded-full mr-3"></span>
                  Chrome Extension (Kinic UI)
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-purple-500 rounded-full mr-3"></span>
                  ICP Backend (vector database)
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-red-500 rounded-full mr-3"></span>
                  PyAutoGUI (mouse/keyboard automation)
                </li>
              </ul>
              <div className="mt-4 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg text-xs">
                <strong>Data Flow:</strong> Base App → API → PyAutoGUI → Chrome Extension → ICP
              </div>
            </div>
          </div>

          {/* Right Panel - Memory Results */}
          <div className="space-y-6">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
              <h2 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">Memory Results</h2>
              
              {memories.length === 0 ? (
                <div className="text-center py-12 text-gray-500 dark:text-gray-400">
                  <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center">
                    🧠
                  </div>
                  <p>No memories retrieved yet</p>
                  <p className="text-sm mt-2">Save pages and search to see your AI memory in action</p>
                </div>
              ) : (
                <div className="space-y-4 max-h-96 overflow-y-auto">
                  {memories.map((memory) => (
                    <div key={memory.id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="font-medium text-gray-800 dark:text-white">Query: {memory.query}</h4>
                        <span className="text-xs text-gray-500 dark:text-gray-400">{memory.timestamp}</span>
                      </div>
                      <div className="text-gray-600 dark:text-gray-300 text-sm bg-gray-50 dark:bg-gray-700 rounded p-3">
                        {memory.response || 'No response received'}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Status */}
        <div className="mt-8 text-center text-gray-500 dark:text-gray-400">
          <p className="flex items-center justify-center space-x-2">
            <span className={`w-2 h-2 rounded-full ${
              apiStatus === 'connected' ? 'bg-green-500' : 
              apiStatus === 'disconnected' ? 'bg-red-500' : 'bg-yellow-500'
            }`}></span>
            <span>
              {apiStatus === 'connected' ? 'Connected to Kinic API (localhost:5006)' :
               apiStatus === 'disconnected' ? 'Kinic API Disconnected - Start with: python kinic-api.py' :
               'Checking Kinic API...'}
            </span>
          </p>
          <p className="text-xs mt-2">
            Base Mini App → Kinic API → Chrome Extension → ICP Backend
          </p>
          {apiStatus === 'disconnected' && (
            <div className="mt-2 p-2 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded text-xs text-red-800 dark:text-red-200">
              ❌ Make sure the Kinic API is running on localhost:5006
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
