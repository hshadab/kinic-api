'use client';

import { useState, useEffect } from 'react';

interface Memory {
  id: string;
  query: string;
  response: string;
  timestamp: string;
}

export default function KinicMiniApp() {
  const [memories, setMemories] = useState<Memory[]>([]);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [agentStatus, setAgentStatus] = useState<'checking' | 'connected' | 'disconnected'>('checking');

  // Check desktop agent status
  useEffect(() => {
    const checkAgent = async () => {
      try {
        const response = await fetch('http://localhost:5007/api/status');
        if (response.ok) {
          const data = await response.json();
          setAgentStatus(data.ready ? 'connected' : 'disconnected');
        } else {
          setAgentStatus('disconnected');
        }
      } catch (error) {
        setAgentStatus('disconnected');
      }
    };

    checkAgent();
    const interval = setInterval(checkAgent, 10000);
    return () => clearInterval(interval);
  }, []);

  const saveCurrentPage = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5007/api/kinic/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          url: window.location.href,
          title: document.title,
          content: document.body.innerText.slice(0, 1000)
        })
      });

      const result = await response.json();

      if (result.success) {
        alert('✅ Page saved to Kinic memory via Chrome extension!');
      } else {
        alert(`❌ Save failed: ${result.error}\n\n💡 ${result.suggestion}`);
      }
    } catch (error) {
      alert(`🔌 Connection error: ${error}\n\n📋 Please ensure:\n• Desktop agent running on localhost:5007\n• Chrome browser open\n• Kinic extension installed`);
    }
    setLoading(false);
  };

  const searchMemory = async () => {
    if (!searchQuery.trim()) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:5007/api/kinic/search-extract', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: searchQuery })
      });

      const result = await response.json();

      if (result.success) {
        setMemories(prev => [...prev, {
          id: result.operation_id || Date.now().toString(),
          query: searchQuery,
          response: result.ai_response || 'No AI response captured',
          timestamp: new Date().toLocaleString()
        }]);
        setSearchQuery('');
      } else {
        alert(`🔍 Search failed: ${result.error}\n\n💡 ${result.suggestion}`);
      }
    } catch (error) {
      alert(`🔌 Connection error: ${error}\n\n📋 Please ensure desktop agent is running`);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      {/* Header */}
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <div className="text-center">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-2">
              Kinic AI Memory
            </h1>
            <p className="text-gray-600 mb-4">Base Mini App - Desktop Agent Integration</p>
            
            {/* Status */}
            <div className="flex items-center justify-center space-x-2 text-sm">
              <span className={`w-3 h-3 rounded-full ${
                agentStatus === 'connected' ? 'bg-green-500' : 
                agentStatus === 'disconnected' ? 'bg-red-500' : 'bg-yellow-500'
              }`}></span>
              <span className={
                agentStatus === 'connected' ? 'text-green-700' : 
                agentStatus === 'disconnected' ? 'text-red-700' : 'text-yellow-700'
              }>
                {agentStatus === 'connected' ? 'Desktop Agent Connected' :
                 agentStatus === 'disconnected' ? 'Desktop Agent Disconnected' :
                 'Checking Desktop Agent...'}
              </span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Memory Operations */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-2xl font-bold mb-4 text-gray-800">Memory Operations</h2>
            
            {/* Save Page */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-2 text-gray-700">Save Current Page</h3>
              <p className="text-gray-600 text-sm mb-3">
                Automate Kinic Chrome extension to save the current page to ICP memory
              </p>
              <button
                onClick={saveCurrentPage}
                disabled={loading || agentStatus !== 'connected'}
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white font-medium py-3 px-4 rounded-lg transition-colors"
              >
                {loading ? '🔄 Automating Chrome Extension...' : '💾 Save Current Page'}
              </button>
            </div>

            {/* Search Memory */}
            <div>
              <h3 className="text-lg font-semibold mb-2 text-gray-700">Search Memory</h3>
              <p className="text-gray-600 text-sm mb-3">
                Query your saved knowledge with AI-powered semantic search
              </p>
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Ask about your saved knowledge..."
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  onKeyPress={(e) => e.key === 'Enter' && searchMemory()}
                  disabled={loading || agentStatus !== 'connected'}
                />
                <button
                  onClick={searchMemory}
                  disabled={loading || !searchQuery.trim() || agentStatus !== 'connected'}
                  className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white font-medium py-2 px-4 rounded-lg transition-colors"
                >
                  {loading ? '🔍' : '🚀 Search'}
                </button>
              </div>
            </div>

            {/* Architecture Info */}
            <div className="mt-6 p-4 bg-blue-50 rounded-lg">
              <h4 className="font-semibold text-blue-800">Architecture</h4>
              <p className="text-blue-700 text-sm mt-1">
                Base Mini App → Desktop Agent → Chrome Extension → ICP
              </p>
              <div className="mt-2 text-xs text-blue-600">
                🖥️ Requires: Desktop agent (localhost:5007) + Kinic Chrome extension
              </div>
            </div>
          </div>

          {/* Memory Results */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-2xl font-bold mb-4 text-gray-800">Memory Results</h2>
            
            {memories.length === 0 ? (
              <div className="text-center py-12 text-gray-500">
                <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center text-2xl">
                  🧠
                </div>
                <p className="font-medium">No memories retrieved yet</p>
                <p className="text-sm mt-2">Save pages and search to see your AI memory in action</p>
                
                {agentStatus === 'disconnected' && (
                  <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                    <p className="font-medium">Desktop Agent Required</p>
                    <p className="mt-1">Please start the desktop agent on your computer to use Kinic memory features.</p>
                  </div>
                )}
              </div>
            ) : (
              <div className="space-y-4 max-h-96 overflow-y-auto">
                {memories.map((memory) => (
                  <div key={memory.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-medium text-gray-800">Query: {memory.query}</h4>
                      <span className="text-xs text-gray-500">{memory.timestamp}</span>
                    </div>
                    <div className="text-gray-600 text-sm bg-gray-50 rounded p-3">
                      {memory.response}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Setup Instructions */}
        {agentStatus === 'disconnected' && (
          <div className="mt-6 bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-3 text-gray-800">🛠️ Setup Required</h3>
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-gray-700 mb-3">To use Kinic memory features, you need to run the desktop agent:</p>
              <ol className="list-decimal list-inside space-y-1 text-sm text-gray-600">
                <li>Download the Kinic Base Integration package</li>
                <li>Run: <code className="bg-gray-200 px-2 py-1 rounded">./setup.sh</code></li>
                <li>Start agent: <code className="bg-gray-200 px-2 py-1 rounded">python kinic-base-agent.py</code></li>
                <li>Ensure Chrome browser is running with Kinic extension</li>
              </ol>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
