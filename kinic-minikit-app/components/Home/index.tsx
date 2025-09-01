"use client";

import { useSignIn } from "@/hooks/use-sign-in";
import Image from "next/image";
import { useState } from "react";

interface Memory {
  id: string;
  query: string;
  response: string;
  timestamp: string;
}

export default function Home() {
  const { signIn, isLoading, isSignedIn, user } = useSignIn({
    autoSignIn: true,
  });
  const [testResult, setTestResult] = useState<string>("");
  const [memories, setMemories] = useState<Memory[]>([]);
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [memoryLoading, setMemoryLoading] = useState<boolean>(false);

  const testAuth = async () => {
    try {
      const res = await fetch("/api/test", {
        credentials: "include",
      });
      const data = await res.json();

      if (!res.ok) {
        setTestResult(`Auth test failed: ${data.error}`);
        return;
      }

      setTestResult(`Auth test succeeded! Server response: ${data.message}`);
    } catch (error) {
      setTestResult(
        "Auth test failed: " +
          (error instanceof Error ? error.message : "Unknown error")
      );
    }
  };

  const saveCurrentPage = async () => {
    if (!isSignedIn) {
      alert('Please sign in first');
      return;
    }
    
    setMemoryLoading(true);
    try {
      // Connect to local Kinic Base Agent
      const response = await fetch('http://localhost:5007/api/kinic/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          url: window.location.href,
          title: document.title,
          content: document.body.innerText.slice(0, 1000) // First 1000 chars
        })
      });
      
      const result = await response.json();
      
      if (result.success) {
        alert('Page saved to Kinic memory via Chrome extension!');
      } else {
        alert(`Failed to save page: ${result.error}\n\nSuggestion: ${result.suggestion}`);
      }
    } catch (error) {
      alert(`Error connecting to Kinic Base Agent: ${error}\n\nPlease ensure the desktop agent is running on localhost:5007`);
    }
    setMemoryLoading(false);
  };

  const searchMemory = async () => {
    if (!isSignedIn || !searchQuery.trim()) return;
    
    setMemoryLoading(true);
    try {
      // Connect to local Kinic Base Agent for search with AI extraction
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
        alert(`Search failed: ${result.error}\n\nSuggestion: ${result.suggestion}`);
      }
    } catch (error) {
      alert(`Error connecting to Kinic Base Agent: ${error}\n\nPlease ensure the desktop agent is running on localhost:5007`);
    }
    setMemoryLoading(false);
  };

  return (
    <div className="bg-gradient-to-br from-blue-50 to-indigo-100 text-black min-h-screen p-4">
      {!isSignedIn ? (
        <div className="flex min-h-screen flex-col items-center justify-center">
          <div className="text-center space-y-6 bg-white p-8 rounded-xl shadow-lg">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
              Kinic AI Memory
            </h1>
            <p className="text-lg text-gray-600">
              AI memory and collaboration on Base
            </p>
            <button
              onClick={signIn}
              disabled={isLoading}
              className="px-8 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
            >
              {isLoading ? "Signing in..." : "Sign in with Farcaster"}
            </button>
          </div>
        </div>
      ) : (
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
            <div className="flex justify-between items-center">
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                  Kinic AI Memory
                </h1>
                <p className="text-gray-600">Base Mini App - Direct ICP Integration</p>
              </div>
              {user && (
                <div className="flex items-center space-x-3">
                  <Image
                    src={user.pfp_url}
                    alt="Profile"
                    className="w-12 h-12 rounded-full"
                    width={48}
                    height={48}
                  />
                  <div className="text-right">
                    <p className="font-semibold">{user.display_name}</p>
                    <p className="text-sm text-gray-500">@{user.username}</p>
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Memory Operations */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-2xl font-bold mb-4">Memory Operations</h2>
              
              {/* Save Page */}
              <div className="mb-6">
                <h3 className="text-lg font-semibold mb-2">Save to Memory</h3>
                <p className="text-gray-600 text-sm mb-3">
                  Save the current page content to your AI memory on ICP
                </p>
                <button
                  onClick={saveCurrentPage}
                  disabled={memoryLoading}
                  className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white font-medium py-3 px-4 rounded-lg transition-colors"
                >
                  {memoryLoading ? 'Saving...' : 'Save Current Page'}
                </button>
              </div>

              {/* Search Memory */}
              <div>
                <h3 className="text-lg font-semibold mb-2">Search Memory</h3>
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
                  />
                  <button
                    onClick={searchMemory}
                    disabled={memoryLoading || !searchQuery.trim()}
                    className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white font-medium py-2 px-4 rounded-lg transition-colors"
                  >
                    {memoryLoading ? '...' : 'Search'}
                  </button>
                </div>
              </div>

              {/* Architecture Info */}
              <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                <h4 className="font-semibold text-blue-800">Architecture</h4>
                <p className="text-blue-700 text-sm mt-1">
                  Base Mini App → Desktop Agent → Chrome Extension → ICP
                </p>
                <p className="text-blue-600 text-xs mt-2">
                  🖥️ Requires: Desktop agent (localhost:5007) + Kinic Chrome extension
                </p>
                <div className="mt-2 text-xs">
                  <span className="inline-block w-2 h-2 bg-blue-500 rounded-full mr-1"></span>
                  <span className="text-blue-600">Hosted mini app connects to user's local agent</span>
                </div>
              </div>
            </div>

            {/* Memory Results */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-2xl font-bold mb-4">Memory Results</h2>
              
              {memories.length === 0 ? (
                <div className="text-center py-12 text-gray-500">
                  <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center text-2xl">
                    🧠
                  </div>
                  <p>No memories retrieved yet</p>
                  <p className="text-sm mt-2">Save pages and search to see your AI memory in action</p>
                </div>
              ) : (
                <div className="space-y-4 max-h-96 overflow-y-auto">
                  {memories.map((memory) => (
                    <div key={memory.id} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="font-medium">Query: {memory.query}</h4>
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

          {/* Debug Section */}
          <div className="mt-6 bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-2">Debug</h3>
            <button
              onClick={testAuth}
              className="px-4 py-2 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 transition-colors"
            >
              Test Authentication
            </button>
            {testResult && (
              <div className="mt-4 p-4 rounded-lg bg-gray-100 text-sm">
                {testResult}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
