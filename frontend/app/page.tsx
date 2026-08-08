"use client";

import React, { useState, useEffect, useCallback } from "react";
import { Navbar } from "@/components/Navbar";
import { OverviewView } from "@/components/OverviewView";
import { FeedView } from "@/components/FeedView";
import { AgentStatusView } from "@/components/AgentStatusView";
import { MemoryView } from "@/components/MemoryView";
import { RejectedTopicsView } from "@/components/RejectedTopicsView";
import { SourcesView } from "@/components/SourcesView";
import { AnalyticsView } from "@/components/AnalyticsView";
import { AIUsageView } from "@/components/AIUsageView";
import { Loader2 } from "lucide-react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [activeTab, setActiveTab] = useState("overview");
  const [isTriggering, setIsTriggering] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // App State
  const [feedPosts, setFeedPosts] = useState<any[]>([]);
  const [agentStatus, setAgentStatus] = useState<any>(null);
  const [memories, setMemories] = useState<any[]>([]);
  const [rejectedTopics, setRejectedTopics] = useState<any[]>([]);
  const [sourcesData, setSourcesData] = useState<any>(null);
  const [analyticsData, setAnalyticsData] = useState<any>(null);
  const [aiUsageData, setAIUsageData] = useState<any>(null);

  // Fetch all live data
  const fetchData = useCallback(async () => {
    try {
      // 1. Feed posts
      const feedRes = await fetch(`${API_BASE}/api/agent/feed`).catch(() => null);
      if (feedRes && feedRes.ok) {
        const data = await feedRes.json();
        setFeedPosts(data.posts || []);
      }

      // 2. Agent status
      const statusRes = await fetch(`${API_BASE}/api/agent/status`).catch(() => null);
      if (statusRes && statusRes.ok) {
        const data = await statusRes.json();
        setAgentStatus(data);
      }

      // 3. Memories
      const memRes = await fetch(`${API_BASE}/api/memory/items`).catch(() => null);
      if (memRes && memRes.ok) {
        const data = await memRes.json();
        setMemories(data || []);
      }

      // 4. Rejected topics
      const rejRes = await fetch(`${API_BASE}/api/rejected/topics`).catch(() => null);
      if (rejRes && rejRes.ok) {
        const data = await rejRes.json();
        setRejectedTopics(data || []);
      }

      // 5. Sources
      const srcRes = await fetch(`${API_BASE}/api/sources`).catch(() => null);
      if (srcRes && srcRes.ok) {
        const data = await srcRes.json();
        setSourcesData(data);
      }

      // 6. Analytics
      const anaRes = await fetch(`${API_BASE}/api/analytics/dashboard`).catch(() => null);
      if (anaRes && anaRes.ok) {
        const data = await anaRes.json();
        setAnalyticsData(data);
      }

      // 7. AI Usage
      const aiRes = await fetch(`${API_BASE}/api/ai-usage`).catch(() => null);
      if (aiRes && aiRes.ok) {
        const data = await aiRes.json();
        setAIUsageData(data);
      }
    } catch (err) {
      console.warn("API fetch error, using local fallback state if needed:", err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000); // 10s auto-refresh
    return () => clearInterval(interval);
  }, [fetchData]);

  // Trigger manual autonomous cycle
  const handleTriggerCycle = async () => {
    setIsTriggering(true);
    try {
      const res = await fetch(`${API_BASE}/api/agent/trigger`, {
        method: "POST",
      });
      if (res.ok) {
        await fetchData();
      }
    } catch (err) {
      console.error("Trigger cycle error:", err);
    } finally {
      setIsTriggering(false);
    }
  };

  // Query memory handler
  const handleQueryMemory = async (query: string) => {
    try {
      const res = await fetch(`${API_BASE}/api/memory/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, limit: 10 }),
      });
      if (res.ok) {
        const data = await res.json();
        return data.matches || [];
      }
    } catch (err) {
      console.error("Query memory error:", err);
    }
    return [];
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col antialiased selection:bg-cyan-500 selection:text-white">
      {/* Top Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onTriggerCycle={handleTriggerCycle}
        isTriggering={isTriggering}
      />

      {/* Main View Container */}
      <main className="flex-1 mx-auto w-full max-w-7xl px-4 py-8 sm:px-6">
        {activeTab === "overview" && (
          <OverviewView
            stats={analyticsData}
            latestPost={feedPosts[0]}
            onNavigate={setActiveTab}
            onTrigger={handleTriggerCycle}
            isTriggering={isTriggering}
          />
        )}

        {activeTab === "feed" && (
          <FeedView
            posts={feedPosts}
            onRefresh={fetchData}
            isLoading={isLoading}
          />
        )}

        {activeTab === "agent" && (
          <AgentStatusView
            statusData={agentStatus}
            onTriggerCycle={handleTriggerCycle}
            isTriggering={isTriggering}
          />
        )}

        {activeTab === "memory" && (
          <MemoryView
            memories={memories}
            onQueryMemory={handleQueryMemory}
          />
        )}

        {activeTab === "rejected" && (
          <RejectedTopicsView
            rejectedTopics={rejectedTopics}
          />
        )}

        {activeTab === "sources" && (
          <SourcesView
            sourcesData={sourcesData}
          />
        )}

        {activeTab === "analytics" && (
          <AnalyticsView
            analyticsData={analyticsData}
          />
        )}

        {activeTab === "ai-usage" && (
          <AIUsageView
            aiUsageData={aiUsageData}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-slate-950 py-6 text-center text-xs text-slate-500">
        <div className="mx-auto max-w-7xl px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p>© 2026 AutoPersona AI • Autonomous Technology Persona Platform</p>
          <div className="flex items-center gap-4 text-slate-400">
            <span>FastAPI Backend</span>
            <span>•</span>
            <span>Next.js 15 App</span>
            <span>•</span>
            <span>Breeth Memory</span>
            <span>•</span>
            <span>LangGraph Engine</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
