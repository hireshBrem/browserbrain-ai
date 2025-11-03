'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2, Bot, User, ChevronDown, ChevronUp, CheckCircle, AlertCircle, Info } from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatUIProps {
  selectedRepo?: { owner: { login: string }; name: string } | null;
  selectedFile?: string | null;
  userGithubToken?: string | null;
}

// Parse ActionResult from string format
interface ActionResult {
  is_done: boolean;
  success: boolean | null;
  error: string | null;
  extracted_content: string;
  long_term_memory: string | null;
  metadata: Record<string, any> | null;
}

interface AgentHistory {
  all_results: ActionResult[];
  all_model_outputs: any[];
}

// Component to display individual action results
const ActionResultCard = ({ result, index, total }: { result: ActionResult; index: number; total: number }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="border-l-4 border-blue-500 bg-blue-50 rounded-r-lg p-4 mb-3">
      <div className="flex items-start justify-between cursor-pointer" onClick={() => setExpanded(!expanded)}>
        <div className="flex items-start gap-3 flex-1">
          <div className="flex-shrink-0 mt-1">
            {result.is_done ? (
              result.success ? (
                <CheckCircle className="h-5 w-5 text-green-600" />
              ) : (
                <AlertCircle className="h-5 w-5 text-red-600" />
              )
            ) : (
              <Info className="h-5 w-5 text-blue-600" />
            )}
          </div>
          <div className="flex-1 min-w-0">
            <h4 className="font-semibold text-gray-900">
              Step {index + 1} of {total}
              {result.is_done && (
                <span className="ml-2 text-xs font-normal bg-green-100 text-green-800 px-2 py-1 rounded">
                  Complete
                </span>
              )}
            </h4>
            <p className="text-sm text-gray-700 mt-1 line-clamp-2">{result.extracted_content}</p>
          </div>
        </div>
        <div className="flex-shrink-0 ml-2">
          {expanded ? (
            <ChevronUp className="h-5 w-5 text-gray-400" />
          ) : (
            <ChevronDown className="h-5 w-5 text-gray-400" />
          )}
        </div>
      </div>

      {expanded && (
        <div className="mt-4 space-y-3 text-sm">
          {result.extracted_content && (
            <div className="bg-white rounded p-2 border border-gray-200">
              <p className="text-xs font-semibold text-gray-600 uppercase">Output</p>
              <p className="text-gray-800 mt-1">{result.extracted_content}</p>
            </div>
          )}

          {result.long_term_memory && (
            <div className="bg-white rounded p-2 border border-gray-200">
              <p className="text-xs font-semibold text-gray-600 uppercase">Memory</p>
              <p className="text-gray-800 mt-1">{result.long_term_memory}</p>
            </div>
          )}

          {result.error && (
            <div className="bg-red-50 rounded p-2 border border-red-200">
              <p className="text-xs font-semibold text-red-600 uppercase">Error</p>
              <p className="text-red-800 mt-1">{result.error}</p>
            </div>
          )}

          {result.metadata && Object.keys(result.metadata).length > 0 && (
            <div className="bg-white rounded p-2 border border-gray-200">
              <p className="text-xs font-semibold text-gray-600 uppercase">Metadata</p>
              <div className="mt-1 space-y-1">
                {Object.entries(result.metadata).map(([key, value]) => (
                  <div key={key} className="flex justify-between text-gray-700">
                    <span className="font-mono text-xs text-gray-600">{key}:</span>
                    <span className="font-mono text-xs text-gray-800">{String(value)}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

// Component to display full agent history
const AgentHistoryComponent = ({ history }: { history: AgentHistory }) => {
  return (
    <div className="space-y-4 w-full">
      <div className="text-sm font-semibold text-gray-700 uppercase tracking-wide">
        Agent Execution Timeline ({history.all_results.length} steps)
      </div>
      <div className="space-y-2">
        {history.all_results.map((result, index) => (
          <ActionResultCard
            key={index}
            result={result}
            index={index}
            total={history.all_results.length}
          />
        ))}
      </div>
    </div>
  );
};

// Try to parse and format message content
const formatMessageContent = (content: string): React.ReactNode => {
  try {
    // Check if it contains AgentHistoryList pattern
    if (content.includes('AgentHistoryList(')) {
      const parsed = parseAgentHistory(content);
      if (parsed) {
        return <AgentHistoryComponent history={parsed} />;
      }
    }

    // Try JSON parsing
    if (content.trim().startsWith('{') || content.trim().startsWith('[')) {
      const parsed = JSON.parse(content);
      return <AgentHistoryComponent history={parsed} />;
    }
  } catch (e) {
    // Continue to default rendering
  }

  // Default: plain text
  return <p className="text-sm whitespace-pre-wrap break-words">{content}</p>;
};

// Parse Python-like AgentHistoryList format
const parseAgentHistory = (content: string): AgentHistory | null => {
  try {
    const allResultsMatch = content.match(/all_results=\[(.*?)\], all_model_outputs/s);
    if (!allResultsMatch) return null;

    const resultsStr = allResultsMatch[1];
    const actionResults: ActionResult[] = [];

    // Split by ActionResult
    const resultMatches = resultsStr.split(/ActionResult\(/);

    for (let i = 1; i < resultMatches.length; i++) {
      const resultStr = resultMatches[i];
      const result: ActionResult = {
        is_done: extractBoolean(resultStr, 'is_done'),
        success: extractBooleanOrNull(resultStr, 'success'),
        error: extractString(resultStr, 'error'),
        extracted_content: extractString(resultStr, 'extracted_content') || '',
        long_term_memory: extractString(resultStr, 'long_term_memory'),
        metadata: extractMetadata(resultStr),
      };
      actionResults.push(result);
    }

    return {
      all_results: actionResults,
      all_model_outputs: [],
    };
  } catch (e) {
    console.error('Parse error:', e);
    return null;
  }
};

const extractString = (str: string, key: string): string | null => {
  const regex = new RegExp(`${key}='([^']*)'`);
  const match = str.match(regex);
  return match ? match[1] : null;
};

const extractBoolean = (str: string, key: string): boolean => {
  const regex = new RegExp(`${key}=(True|False)`);
  const match = str.match(regex);
  return match ? match[1] === 'True' : false;
};

const extractBooleanOrNull = (str: string, key: string): boolean | null => {
  const regex = new RegExp(`${key}=(True|False|None)`);
  const match = str.match(regex);
  if (!match) return null;
  if (match[1] === 'None') return null;
  return match[1] === 'True';
};

const extractMetadata = (str: string): Record<string, any> | null => {
  const regex = /metadata=({[^}]*}|None)/;
  const match = str.match(regex);
  if (!match || match[1] === 'None') return null;

  try {
    // Try to parse metadata as JSON-like
    const metaStr = match[1].replace(/'/g, '"');
    return JSON.parse(metaStr);
  } catch {
    return null;
  }
};

export function ChatUI({ selectedRepo, selectedFile, userGithubToken }: ChatUIProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const messageToSend = input.trim();
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: messageToSend,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:4000/agent/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: messageToSend,
        }),
      });

      if (!response.ok) throw new Error('Failed to get response');

      const data = await response.json();
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.message,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-screen w-screen bg-white">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 w-full max-w-4xl mx-auto hide-scrollbar">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-gray-600 text-center px-4">
            <Bot className="h-12 w-12 mb-4 opacity-50 text-gray-400" />
            <p className="text-xs text-gray-500">
              {/* Ask me anything about your repository, code, or files! */}
            </p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex gap-3 ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {message.role === 'assistant' && (
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center">
                  <Bot className="h-4 w-4 text-gray-700" />
                </div>
              )}
              <div
                className={`rounded-lg p-4 ${
                  message.role === 'user'
                    ? 'bg-blue-500 text-white max-w-[80%]'
                    : 'bg-gray-50 text-gray-900 w-full'
                }`}
              >
                {message.role === 'assistant'
                  ? formatMessageContent(message.content)
                  : <p className="text-sm whitespace-pre-wrap break-words">{message.content}</p>}
                <p className={`text-xs mt-2 ${message.role === 'user' ? 'text-blue-100' : 'text-gray-500'}`}>
                  {message.timestamp.toLocaleTimeString()}
                </p>
              </div>
              {message.role === 'user' && (
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center">
                  <User className="h-4 w-4 text-white" />
                </div>
              )}
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex gap-3 justify-start">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center">
              <Bot className="h-4 w-4 text-gray-700" />
            </div>
            <div className="bg-gray-50 text-gray-900 rounded-lg p-4">
              <Loader2 className="h-4 w-4 animate-spin" />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t border-gray-200 bg-white w-full max-w-4xl mx-auto">
        <div className="flex gap-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Ask about your repository..."
            disabled={isLoading}
            className="flex-1 px-3 py-2 bg-white border border-gray-300 rounded text-sm text-gray-900 placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 resize-none"
            rows={2}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-300 disabled:text-gray-500 transition-colors flex items-center justify-center"
          >
            {isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

