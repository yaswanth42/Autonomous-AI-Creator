"use client";

import React, { useState } from "react";
import {
  Terminal,
  Cpu,
  Clock,
  Zap,
  Activity,
  Layers,
  CheckCircle2,
  Code2,
} from "lucide-react";
import { formatDate } from "@/lib/utils";

interface AIUsageViewProps {
  aiUsageData: any;
}

export const AIUsageView: React.FC<AIUsageViewProps> = ({ aiUsageData }) => {
  const summary = aiUsageData?.summary || {
    total_prompts: 4,
    total_tokens: 3840,
    average_latency_ms: 184.2,
    model: "gpt-4o-mini",
  };

  const logs = aiUsageData?.logs || [];
  const [selectedLog, setSelectedLog] = useState<any | null>(null);

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Header */}
      <div className="border-b border-slate-800/80 pb-4">
        <h2 className="text-2xl font-bold tracking-tight text-white">AI-Usage Log & Execution Telemetry</h2>
        <p className="text-xs text-slate-400 mt-1">
          Complete audit trail tracking every model prompt, token consumption, latency, and milestone.
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {[
          { label: "Total Prompts Logged", val: summary.total_prompts, icon: Terminal, color: "text-cyan-400" },
          { label: "Total Tokens", val: summary.total_tokens?.toLocaleString() || "0", icon: Zap, color: "text-amber-400" },
          { label: "Avg Latency", val: `${summary.average_latency_ms || 180} ms`, icon: Clock, color: "text-emerald-400" },
          { label: "Primary Model", val: summary.model || "gpt-4o-mini", icon: Cpu, color: "text-purple-400" },
        ].map((c, i) => {
          const Icon = c.icon;
          return (
            <div
              key={i}
              className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4 backdrop-blur-xl space-y-1"
            >
              <div className="flex items-center justify-between text-slate-400">
                <span className="text-xs">{c.label}</span>
                <Icon className={`h-4 w-4 ${c.color}`} />
              </div>
              <div className="text-xl font-bold text-white font-mono">{c.val}</div>
            </div>
          );
        })}
      </div>

      {/* Telemetry Logs Table */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/70 overflow-hidden shadow-xl">
        <div className="border-b border-slate-800 px-6 py-3 flex items-center justify-between bg-slate-950/40">
          <div className="flex items-center gap-2 text-xs font-semibold text-slate-200">
            <Activity className="h-4 w-4 text-cyan-400" />
            <span>AI Prompt Audit Trail</span>
          </div>
          <span className="text-xs text-slate-400 font-mono">{logs.length} Executions</span>
        </div>

        <div className="divide-y divide-slate-800/60 max-h-[500px] overflow-y-auto">
          {logs.map((log: any) => (
            <div
              key={log.id}
              onClick={() => setSelectedLog(log)}
              className="p-4 hover:bg-slate-800/40 cursor-pointer transition-colors space-y-2"
            >
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <span className="rounded-md bg-cyan-950/80 px-2 py-0.5 text-[10px] font-mono font-semibold text-cyan-300 border border-cyan-500/30">
                    {log.milestone || "Prompt Execution"}
                  </span>
                  <span className="font-semibold text-xs text-slate-200">{log.prompt_title}</span>
                </div>
                <div className="flex items-center gap-3 text-[11px] font-mono text-slate-400">
                  <span>{log.tokens_used} tokens</span>
                  <span>•</span>
                  <span className="text-emerald-400">{log.latency_ms} ms</span>
                  <span>•</span>
                  <span>{formatDate(log.timestamp)}</span>
                </div>
              </div>

              <p className="text-xs text-slate-400 line-clamp-2 font-mono">
                {log.output_summary}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Selected Log Modal */}
      {selectedLog && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4 backdrop-blur-sm">
          <div className="relative w-full max-w-2xl rounded-2xl border border-slate-700 bg-slate-900 p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-sm font-bold text-white">{selectedLog.prompt_title}</h3>
              <button
                onClick={() => setSelectedLog(null)}
                className="rounded-lg bg-slate-800 px-2 py-1 text-xs text-slate-400 hover:text-white"
              >
                Close
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div>
                <span className="text-slate-400 font-mono">Prompt Text:</span>
                <div className="mt-1 rounded-xl bg-slate-950 p-3 font-mono text-slate-300 max-h-40 overflow-y-auto border border-slate-800">
                  {selectedLog.prompt_text}
                </div>
              </div>

              <div>
                <span className="text-slate-400 font-mono">Output Summary:</span>
                <div className="mt-1 rounded-xl bg-slate-950 p-3 font-mono text-cyan-300 max-h-40 overflow-y-auto border border-slate-800">
                  {selectedLog.output_summary}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
