"use client";

import React from "react";
import {
  Globe,
  Search,
  ShieldCheck,
  ExternalLink,
  History,
  Tag,
  Clock,
  Layers,
} from "lucide-react";
import { formatDate } from "@/lib/utils";

interface SourcesViewProps {
  sourcesData: any;
}

export const SourcesView: React.FC<SourcesViewProps> = ({ sourcesData }) => {
  const keywords = sourcesData?.keywords || [
    "Artificial Intelligence",
    "LLM",
    "Machine Learning",
    "Open Source AI",
    "Google DeepMind",
    "OpenAI",
    "Anthropic",
    "Microsoft AI",
    "Meta AI",
    "HuggingFace",
    "MCP",
  ];

  const authorities = sourcesData?.trusted_authorities || [
    { name: "Anthropic Research", domain: "research.anthropic.com", trust_tier: "TIER_1", status: "ACTIVE" },
    { name: "Google DeepMind", domain: "deepmind.google", trust_tier: "TIER_1", status: "ACTIVE" },
    { name: "OpenAI Safety & Alignment", domain: "openai.com/research", trust_tier: "TIER_1", status: "ACTIVE" },
    { name: "Meta AI Research", domain: "ai.meta.com/research", trust_tier: "TIER_1", status: "ACTIVE" },
    { name: "HuggingFace Security", domain: "huggingface.co/blog", trust_tier: "TIER_1", status: "ACTIVE" },
    { name: "Microsoft Research", domain: "microsoft.com/research", trust_tier: "TIER_1", status: "ACTIVE" },
    { name: "arXiv CS.CR / AI", domain: "arxiv.org", trust_tier: "TIER_1", status: "ACTIVE" },
    { name: "OWASP GenAI Security", domain: "owasp.org", trust_tier: "TIER_1", status: "ACTIVE" },
  ];

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Header */}
      <div className="border-b border-slate-800/80 pb-4">
        <h2 className="text-2xl font-bold tracking-tight text-white">Discovery Sources & Curated Authorities</h2>
        <p className="text-xs text-slate-400 mt-1">
          Authoritative intelligence origins and curated keyword streams used by Tavily Search.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Curated Keywords */}
        <div className="lg:col-span-1 rounded-2xl border border-slate-800 bg-slate-900/70 p-6 backdrop-blur-xl shadow-xl space-y-4">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
            <Tag className="h-4 w-4 text-cyan-400" />
            <span>Target AI Keywords ({keywords.length})</span>
          </div>

          <div className="flex flex-wrap gap-2">
            {keywords.map((kw: string, i: number) => (
              <span
                key={i}
                className="rounded-lg bg-cyan-950/40 px-3 py-1.5 text-xs font-medium text-cyan-300 border border-cyan-500/30 transition-all hover:bg-cyan-900/50"
              >
                #{kw}
              </span>
            ))}
          </div>
        </div>

        {/* Authoritative Domains */}
        <div className="lg:col-span-2 rounded-2xl border border-slate-800 bg-slate-900/70 p-6 backdrop-blur-xl shadow-xl space-y-4">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
            <ShieldCheck className="h-4 w-4 text-emerald-400" />
            <span>Authoritative AI Research & Security Domains</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {authorities.map((auth: any, idx: number) => (
              <div
                key={idx}
                className="flex items-center justify-between p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80 transition-all hover:border-slate-700"
              >
                <div className="space-y-0.5">
                  <h4 className="text-xs font-bold text-slate-200">{auth.name}</h4>
                  <p className="text-[11px] text-slate-400 font-mono">{auth.domain}</p>
                </div>
                <div className="flex items-center gap-2">
                  <span className="rounded-md bg-emerald-950/80 px-2 py-0.5 text-[10px] font-semibold text-emerald-400 border border-emerald-500/30">
                    {auth.trust_tier}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
