"use client";

import { useEffect, useState } from "react";

interface ApiResponse {
  message?: string;
  status?: string;
}

interface AgentResponse {
  message?: string;
}

export default function Home() {
  const [message, setMessage] = useState<string>("");
  const [health, setHealth] = useState<string>("");
  const [agentResult, setAgentResult] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(true);
  const [agentLoading, setAgentLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

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
      
      const response = await fetch("http://localhost:4000/agent/execute");
      const data: AgentResponse = await response.json();
      setAgentResult(data.message || "No result returned");
    } catch (err) {
      setError("Failed to execute agent. Make sure the server is running on port 4000.");
      console.error("Error executing agent:", err);
    } finally {
      setAgentLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex min-h-screen w-full max-w-3xl flex-col items-center justify-center py-32 px-16 bg-white dark:bg-black">
        <div className="flex flex-col items-center gap-8 text-center">
          <h1 className="text-4xl font-bold leading-tight tracking-tight text-black dark:text-zinc-50">
            Redis Hackathon App
          </h1>

          {loading && (
            <p className="text-lg text-zinc-600 dark:text-zinc-400">
              Loading...
            </p>
          )}

          {error && (
            <div className="rounded-lg bg-red-50 dark:bg-red-900/20 p-4">
              <p className="text-red-800 dark:text-red-200">{error}</p>
            </div>
          )}

          {!loading && !error && (
            <div className="flex flex-col gap-6 w-full max-w-md">
              <div className="rounded-lg bg-zinc-100 dark:bg-zinc-900 p-6">
                <h2 className="text-xl font-semibold mb-2 text-black dark:text-zinc-50">
                  API Message
                </h2>
                <p className="text-zinc-700 dark:text-zinc-300">
                  {message}
                </p>
              </div>

              <div className="rounded-lg bg-green-100 dark:bg-green-900/20 p-6">
                <h2 className="text-xl font-semibold mb-2 text-black dark:text-zinc-50">
                  Health Status
                </h2>
                <p className="text-zinc-700 dark:text-zinc-300">
                  {health}
                </p>
              </div>

              <div className="rounded-lg bg-blue-100 dark:bg-blue-900/20 p-6">
                <h2 className="text-xl font-semibold mb-4 text-black dark:text-zinc-50">
                  Agent Execution
                </h2>
                <button
                  onClick={executeAgent}
                  disabled={agentLoading}
                  className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white rounded-lg font-medium transition-colors"
                >
                  {agentLoading ? "Executing..." : "Execute Agent"}
                </button>
                {agentResult && (
                  <div className="mt-4 p-4 bg-white dark:bg-zinc-800 rounded-lg">
                    <p className="text-sm text-zinc-600 dark:text-zinc-400 mb-2">Result:</p>
                    <p className="text-zinc-700 dark:text-zinc-300 whitespace-pre-wrap">
                      {agentResult}
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
