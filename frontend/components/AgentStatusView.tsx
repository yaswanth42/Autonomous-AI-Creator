"use client";

import React, { useState } from "react";
import {
  Bot,
  Shield,
  Clock,
  Play,
  Pause,
  RefreshCw,
  CheckCircle,
  FileCode,
  Sliders,
  Cpu,
  Layers,
  Sparkles,
  Zap,
} from "lucide-react";
import { formatDate } from "@/lib/utils";

interface AgentStatusViewProps {
  statusData: any;
  onTriggerCycle: () => void;
  isTriggering: boolean;
}

export const AgentStatusView: React.FC<AgentStatusViewProps> = ({
  statusData,
  onTriggerCycle,
  isTriggering,
}) => {
  const agent = statusData?.agent || {
    name: "Ada",
    domain: "AI Security",
    characteristics: [
      "Professional",
      "Research based",
      "Technical",
      "Friendly",
      "Opinionated",
      "Avoid clickbait",
      "Always explain",
      "Always cite sources",
      "Maintain same tone in every post",
    ],
    status: "ACTIVE",
    system_prompt: "Autonomous AI persona specialized in AI Security and Systems Architecture.",
  };

  const scheduler = statusData?.scheduler || {
    is_running: true,
    cadence_hours: 4,
    next_run_time: null,
    last_run_time: null,
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Header */}
      <div className="border-b border-slate-800/80 pb-4">
        <h2 className="text-2xl font-bold tracking-tight text-white">Agent Persona & Scheduler Control</h2>
        <p className="text-xs text-slate-400 mt-1">
          Real-time telemetry, cognitive policies, and autonomous scheduler status for Ada.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Profile Card */}
        <div className="lg:col-span-1 space-y-6">
          <div className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/70 p-6 backdrop-blur-xl shadow-xl">
            <div className="flex flex-col items-center text-center pb-6 border-b border-slate-800/80">
              <div className="relative mb-3 flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-tr from-cyan-500 via-blue-600 to-indigo-600 shadow-xl shadow-cyan-500/25 ring-2 ring-white/20">
                <Bot className="h-10 w-10 text-white" />
                <span className="absolute bottom-0 right-0 flex h-4 w-4">
                  <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex h-4 w-4 rounded-full bg-emerald-500"></span>
                </span>
              </div>
              <h3 className="text-xl font-bold text-white">{agent.name}</h3>
              <p className="text-xs font-medium text-cyan-400 mt-0.5">{agent.domain}</p>
              <div className="mt-3 inline-flex items-center gap-1.5 rounded-full bg-emerald-950/80 px-3 py-1 text-xs font-semibold text-emerald-400 border border-emerald-500/30">
                <CheckCircle className="h-3.5 w-3.5" />
                <span>Status: {agent.status || "ACTIVE"}</span>
              </div>
            </div>

            {/* Persona Characteristics */}
            <div className="pt-5 space-y-3">
              <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                <Shield className="h-3.5 w-3.5 text-cyan-400" />
                Cognitive Persona Traits
              </h4>
              <div className="flex flex-wrap gap-1.5">
                {(agent.characteristics || []).map((trait: string, idx: number) => (
                  <span
                    key={idx}
                    className="rounded-lg bg-slate-800/90 px-2.5 py-1 text-[11px] font-medium text-slate-200 border border-slate-700/60"
                  >
                    {trait}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Scheduler Status Card */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 backdrop-blur-xl shadow-xl space-y-4">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <Clock className="h-3.5 w-3.5 text-cyan-400" />
              APScheduler Cadence
            </h4>

            <div className="space-y-3 text-xs">
              <div className="flex items-center justify-between py-2 border-b border-slate-800/60">
                <span className="text-slate-400">Autonomous Cycle:</span>
                <span className="font-semibold text-slate-100">Every {scheduler.cadence_hours || 4} Hours</span>
              </div>
              <div className="flex items-center justify-between py-2 border-b border-slate-800/60">
                <span className="text-slate-400">Scheduler State:</span>
                <span className="font-semibold text-emerald-400 flex items-center gap-1">
                  <span className="h-1.5 w-1.5 rounded-full bg-emerald-400"></span>
                  Running (Background)
                </span>
              </div>
              <div className="flex items-center justify-between py-2 border-b border-slate-800/60">
                <span className="text-slate-400">Last Execution:</span>
                <span className="font-mono text-slate-300">{formatDate(scheduler.last_run_time)}</span>
              </div>
            </div>

            <button
              onClick={onTriggerCycle}
              disabled={isTriggering}
              className="w-full flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 py-2.5 text-xs font-semibold text-white shadow-lg shadow-cyan-500/20 hover:scale-[1.02] transition-all disabled:opacity-50"
            >
              <Zap className="h-4 w-4" />
              {isTriggering ? "Executing Cycle..." : "Execute Cycle Immediately"}
            </button>
          </div>
        </div>

        {/* System Prompt & Cognitive Architecture */}
        <div className="lg:col-span-2 space-y-6">
          <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 backdrop-blur-xl shadow-xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
              <div className="flex items-center gap-2">
                <FileCode className="h-4 w-4 text-cyan-400" />
                <h3 className="text-sm font-semibold text-slate-200">System Prompt & Instruction Mandate</h3>
              </div>
              <span className="rounded-md bg-slate-800 px-2 py-0.5 text-[10px] font-mono text-slate-400">
                Prompt 6 Spec
              </span>
            </div>

            <div className="rounded-xl bg-slate-950/80 p-4 border border-slate-800 font-mono text-xs text-slate-300 leading-relaxed max-h-96 overflow-y-auto whitespace-pre-line">
              {agent.system_prompt}
            </div>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 backdrop-blur-xl shadow-xl space-y-4">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <Cpu className="h-3.5 w-3.5 text-cyan-400" />
              LangGraph State Machine Specifications
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs text-slate-300">
              <div className="rounded-xl bg-slate-950/60 p-3 border border-slate-800/80 space-y-1">
                <span className="font-semibold text-cyan-300">1. Breeth Memory Interlock</span>
                <p className="text-[11px] text-slate-400">Queries TF-IDF semantic embeddings before accepting new candidate topics to guarantee zero duplicate posting.</p>
              </div>
              <div className="rounded-xl bg-slate-950/60 p-3 border border-slate-800/80 space-y-1">
                <span className="font-semibold text-blue-300">2. 7-Factor Editorial Gate</span>
                <p className="text-[11px] text-slate-400">Weights Novelty, Importance, Trustworthiness, Technical Value, and Community Impact with a 7.0 cutoff.</p>
              </div>
              <div className="rounded-xl bg-slate-950/60 p-3 border border-slate-800/80 space-y-1">
                <span className="font-semibold text-purple-300">3. LinkedIn Post Refinement</span>
                <p className="text-[11px] text-slate-400">Formats 200-350 words: Title, Hook, Deep Body, 3 Key Insights, and Strategic Takeaway with citations.</p>
              </div>
              <div className="rounded-xl bg-slate-950/60 p-3 border border-slate-800/80 space-y-1">
                <span className="font-semibold text-emerald-300">4. Auto-Persistence & Feed Sync</span>
                <p className="text-[11px] text-slate-400">Simultaneously writes to SQLite Posts table and registers semantic vectors in Breeth Memory store.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
