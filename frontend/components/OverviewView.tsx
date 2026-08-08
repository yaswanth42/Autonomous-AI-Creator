"use client";

import React from "react";
import {
  Sparkles,
  Bot,
  Brain,
  ShieldAlert,
  Send,
  ArrowRight,
  Clock,
  CheckCircle2,
  Cpu,
  Layers,
  Flame,
  Search,
} from "lucide-react";
import { formatDate } from "@/lib/utils";

interface OverviewViewProps {
  stats: any;
  latestPost: any;
  onNavigate: (tab: string) => void;
  onTrigger: () => void;
  isTriggering: boolean;
}

export const OverviewView: React.FC<OverviewViewProps> = ({
  stats,
  latestPost,
  onNavigate,
  onTrigger,
  isTriggering,
}) => {
  const cards = stats?.cards || {};

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Hero Banner */}
      <div className="relative overflow-hidden rounded-3xl border border-cyan-500/20 bg-gradient-to-b from-slate-900/90 via-slate-900/60 to-slate-950/90 p-6 sm:p-8 backdrop-blur-xl shadow-2xl">
        <div className="absolute -top-24 -right-24 h-72 w-72 rounded-full bg-cyan-500/10 blur-3xl pointer-events-none"></div>
        <div className="absolute -bottom-24 -left-24 h-72 w-72 rounded-full bg-indigo-500/10 blur-3xl pointer-events-none"></div>

        <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="space-y-3">
            <div className="inline-flex items-center gap-2 rounded-full bg-cyan-500/10 px-3 py-1 text-xs font-semibold text-cyan-400 border border-cyan-500/20">
              <span className="h-2 w-2 rounded-full bg-cyan-400 animate-pulse"></span>
              Autonomous Agent Live • 4-Hour APScheduler Loop
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-white">
              Autonomous Persona <span className="bg-gradient-to-r from-cyan-400 via-blue-400 to-indigo-400 bg-clip-text text-transparent">Ada</span>
            </h1>
            <p className="max-w-2xl text-sm sm:text-base text-slate-300">
              Ada continuously scouts breakthrough AI research, filters noise via a 7-factor editorial decision engine, consults Breeth Memory before making decisions, and publishes technical LinkedIn-style analyses autonomously.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
            <button
              onClick={() => onNavigate("feed")}
              className="flex items-center justify-center gap-2 rounded-xl bg-slate-800/80 px-4 py-2.5 text-xs font-semibold text-white border border-slate-700/80 hover:bg-slate-700 transition-all"
            >
              <Send className="h-4 w-4 text-cyan-400" />
              View Feed
            </button>
            <button
              onClick={onTrigger}
              disabled={isTriggering}
              className="flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 px-5 py-2.5 text-xs font-semibold text-white shadow-lg shadow-cyan-500/25 hover:shadow-cyan-500/40 hover:scale-[1.02] transition-all disabled:opacity-50"
            >
              <Sparkles className="h-4 w-4" />
              {isTriggering ? "Running Cycle..." : "Trigger Autonomous Cycle"}
            </button>
          </div>
        </div>

        {/* 5-Step Pipeline Visualizer */}
        <div className="mt-8 border-t border-slate-800/80 pt-6">
          <p className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-4 flex items-center gap-2">
            <Cpu className="h-3.5 w-3.5 text-cyan-400" />
            Autonomous Decision Pipeline
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-5 gap-3">
            {[
              { step: "01", name: "Tavily Search", desc: "11 AI Keywords Scanned", icon: Search, color: "text-cyan-400 border-cyan-500/30 bg-cyan-950/40" },
              { step: "02", name: "Breeth Memory", desc: "Duplicate & Novelty Check", icon: Brain, color: "text-purple-400 border-purple-500/30 bg-purple-950/40" },
              { step: "03", name: "Editorial Engine", desc: "7-Factor Scoring (Cutoff 7.0)", icon: ShieldAlert, color: "text-amber-400 border-amber-500/30 bg-amber-950/40" },
              { step: "04", name: "LangGraph / Ada", desc: "LinkedIn Markdown 200-350w", icon: Bot, color: "text-blue-400 border-blue-500/30 bg-blue-950/40" },
              { step: "05", name: "Autonomous Publish", desc: "Internal Feed & Memory Sync", icon: CheckCircle2, color: "text-emerald-400 border-emerald-500/30 bg-emerald-950/40" },
            ].map((p, idx) => {
              const Icon = p.icon;
              return (
                <div
                  key={idx}
                  className={`flex flex-col p-3 rounded-xl border ${p.color} transition-all hover:scale-[1.02]`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-[10px] font-mono text-slate-400">Step {p.step}</span>
                    <Icon className="h-3.5 w-3.5" />
                  </div>
                  <h4 className="text-xs font-bold text-slate-100">{p.name}</h4>
                  <p className="text-[11px] text-slate-400 mt-0.5">{p.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
        {[
          { label: "Posts Published", val: cards.posts_published?.value ?? "2", sub: cards.posts_published?.change ?? "Active", icon: Send, color: "text-cyan-400" },
          { label: "Breeth Memory", val: cards.memory_usage?.value ?? "5", sub: cards.memory_usage?.change ?? "Nodes Indexed", icon: Brain, color: "text-purple-400" },
          { label: "Topics Rejected", val: cards.topics_rejected?.value ?? "1", sub: cards.topics_rejected?.change ?? "Quality Gate", icon: ShieldAlert, color: "text-amber-400" },
          { label: "Searches Run", val: cards.searches_conducted?.value ?? "4", sub: cards.searches_conducted?.change ?? "Hourly Tavily", icon: Search, color: "text-blue-400" },
          { label: "Acceptance Rate", val: cards.publishing_success_rate?.value ?? "66.7%", sub: "Threshold >= 7.0", icon: Flame, color: "text-emerald-400" },
        ].map((c, i) => {
          const Icon = c.icon;
          return (
            <div
              key={i}
              className="relative overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/60 p-4 backdrop-blur-lg hover:border-slate-700 transition-all hover:translate-y-[-2px]"
            >
              <div className="flex items-center justify-between text-slate-400 mb-2">
                <span className="text-xs font-medium text-slate-400">{c.label}</span>
                <Icon className={`h-4 w-4 ${c.color}`} />
              </div>
              <div className="text-2xl font-bold text-white tracking-tight">{c.val}</div>
              <div className="text-[11px] text-slate-400 mt-1">{c.sub}</div>
            </div>
          );
        })}
      </div>

      {/* Latest Published Post Highlight */}
      {latestPost && (
        <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 backdrop-blur-xl space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
            <div className="flex items-center gap-2">
              <span className="inline-flex h-2.5 w-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
              <h3 className="text-sm font-semibold text-slate-200">Latest Autonomous Publication</h3>
              <span className="text-xs text-slate-400 font-mono">
                {formatDate(latestPost.createdAt || latestPost.published_at)}
              </span>
            </div>
            <button
              onClick={() => onNavigate("feed")}
              className="flex items-center gap-1 text-xs font-medium text-cyan-400 hover:text-cyan-300"
            >
              Open Feed <ArrowRight className="h-3.5 w-3.5" />
            </button>
          </div>

          <div className="space-y-2">
            <h2 className="text-lg font-bold text-white">{latestPost.title || "Latest AI Security Breakthrough"}</h2>
            <p className="text-xs text-slate-300 whitespace-pre-line line-clamp-4 font-sans leading-relaxed">
              {latestPost.text || latestPost.raw_markdown}
            </p>
          </div>

          {latestPost.rationale && (
            <div className="rounded-xl bg-slate-950/60 p-3 border border-slate-800/80 text-xs text-slate-400">
              <span className="font-semibold text-cyan-300">Ada Editorial Rationale: </span>
              {latestPost.rationale}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
