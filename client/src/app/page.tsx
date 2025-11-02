"use client";

import { useEffect, useState } from "react";
import { ChatUI } from "@/components/ChatUI";

interface ApiResponse {
  message?: string;
  status?: string;
}

interface AgentStep {
  step: number;
  description: string;
  is_done: boolean;
  success?: boolean | null;
}

interface AgentResponse {
  summary: string;
  steps: AgentStep[];
  success: boolean;
  error?: string;
}

export default function Home() {
  const [message, setMessage] = useState<string>("");
  const [health, setHealth] = useState<string>("");
  const [agentData, setAgentData] = useState<AgentResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [agentLoading, setAgentLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");
  const [themeColor, setThemeColor] = useState("#6366f1");

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError("");

        // Fetch main endpoint
        const response = await fetch("http://localhost:4000/");
        const data: ApiResponse = await response.json();
        setMessage(data.message || "");

        // Fetch health endpoint
        const healthResponse = await fetch("http://localhost:4000/health");
        const healthData: ApiResponse = await healthResponse.json();
        setHealth(healthData.status || "");
      } catch (err) {
        console.log('err: ', err);
        setError("Failed to fetch data from API. Make sure the server is running on port 4000.");
        console.error("Error fetching data:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const executeAgent = async () => {
    try {
      setAgentLoading(true);
      setError("");
      setAgentData(null);

      const response = await fetch("http://localhost:4000/agent/execute");
    //   if (!response.ok) {
    //     throw new Error(`Agent request failed with status ${response.status}`);
    //   }

      const data: AgentResponse = await response.json();
      setAgentData(data);
      console.log('data: ', data);
    } catch (err) {
      setError("Failed to execute agent. Make sure the server is running on port 4000.");
      console.error("Error executing agent:", err);
    } finally {
      setAgentLoading(false);
    }
  };

  return (
    <div
      style={{ backgroundColor: themeColor }}
      className="h-screen w-screen flex justify-center items-center flex-col transition-colors duration-300"
    >
      <div className="bg-white/20 backdrop-blur-md p-8 rounded-2xl shadow-xl max-w-2xl w-full">
        <h1 className="text-4xl font-bold text-white mb-2 text-center">
          Redis Hackathon App
        </h1>
        <p className="text-gray-200 text-center italic mb-6">
          Browser Agent Context Enhancement 🪁
        </p>
        <hr className="border-white/20 my-6" />

        {loading && (
          <div className="text-center">
            <p className="text-white animate-pulse">Loading...</p>
          </div>
        )}

        {error && (
          <div className="bg-red-500/20 backdrop-blur-sm p-4 rounded-xl mb-4">
            <p className="text-white">{error}</p>
          </div>
        )}

        {!loading && !error && (
          <div className="flex flex-col gap-4">
            {message && (
              <div className="bg-white/15 p-4 rounded-xl text-white">
                <h2 className="text-lg font-semibold mb-2">API Message</h2>
                <p className="text-white/90">{message}</p>
              </div>
            )}

            {health && (
              <div className="bg-white/15 p-4 rounded-xl text-white">
                <h2 className="text-lg font-semibold mb-2">Health Status</h2>
                <p className="text-white/90">{health}</p>
              </div>
            )}

            <div className="bg-white/15 p-4 rounded-xl text-white">
              <h2 className="text-lg font-semibold mb-4">Agent Execution</h2>
              <button
                onClick={executeAgent}
                disabled={agentLoading}
                className="w-full px-4 py-3 bg-white/20 hover:bg-white/30 disabled:bg-white/10 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-all backdrop-blur-sm"
              >
                {agentLoading ? "Executing..." : "Execute Agent"}
              </button>

              {agentData && (
                <div className="mt-4 space-y-4">
                  <div className="bg-white/10 p-4 rounded-xl">
                    <p className="text-sm font-medium text-white mb-3">Complete Agent Response</p>
                    <div className="bg-black/20 p-3 rounded-lg overflow-auto max-h-96">
                      <pre className="text-xs text-white/90 whitespace-pre-wrap break-words">
                        {JSON.stringify(agentData, null, 2)}
                      </pre>
                    </div>
                  </div>
                </div>
              )}
            </div>

            <div className="bg-white/15 p-4 rounded-xl text-white">
              <h2 className="text-lg font-semibold mb-4">Chat UI</h2>
              <div className="h-[600px] bg-black/20 rounded-lg overflow-hidden">
                <ChatUI />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
