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

      const response = await fetch("http://localhost:4000/agent/chat", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: message,
        }),
      });
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
    <div className="h-screen w-screen bg-white">
      <ChatUI />
    </div>
  );
}
