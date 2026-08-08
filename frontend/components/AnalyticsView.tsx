"use client";

import React from "react";
import {
  BarChart3,
  TrendingUp,
  PieChart,
  Award,
  Send,
  Brain,
  ShieldAlert,
  Search,
  Flame,
  CheckCircle2,
} from "lucide-react";

interface AnalyticsViewProps {
  analyticsData: any;
}

export const AnalyticsView: React.FC<AnalyticsViewProps> = ({ analyticsData }) => {
  const cards = analyticsData?.cards || {};
  const daily = analyticsData?.daily_publishing || [];
  const categories = analyticsData?.topic_categories || [];
  const sources = analyticsData?.source_distribution || [];
  const scoreTrends = analyticsData?.editorial_score_trends || [];

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Header */}
      <div className="border-b border-slate-800/80 pb-4">
        <h2 className="text-2xl font-bold tracking-tight text-white">System Analytics & Editorial Telemetry</h2>
        <p className="text-xs text-slate-400 mt-1">
          Quantitative metrics covering publishing acceptance, topic clustering, and quality scoring trends.
        </p>
      </div>

      {/* 5 Key Metric Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
        {[
          { label: "Posts Published", val: cards.posts_published?.value ?? "2", sub: cards.posts_published?.change ?? "Active", icon: Send, color: "text-cyan-400" },
          { label: "Breeth Memory", val: cards.memory_usage?.value ?? "5", sub: cards.memory_usage?.change ?? "Nodes", icon: Brain, color: "text-purple-400" },
          { label: "Topics Rejected", val: cards.topics_rejected?.value ?? "1", sub: cards.topics_rejected?.change ?? "Quality Gate", icon: ShieldAlert, color: "text-amber-400" },
          { label: "Searches Run", val: cards.searches_conducted?.value ?? "4", sub: cards.searches_conducted?.change ?? "Hourly Tavily", icon: Search, color: "text-blue-400" },
          { label: "Acceptance Rate", val: cards.publishing_success_rate?.value ?? "66.7%", sub: "Threshold >= 7.0", icon: Flame, color: "text-emerald-400" },
        ].map((c, i) => {
          const Icon = c.icon;
          return (
            <div
              key={i}
              className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/70 p-4 backdrop-blur-xl transition-all hover:border-slate-700 hover:translate-y-[-2px] shadow-lg"
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

      {/* Visual Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Daily Publishing Trends */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 backdrop-blur-xl shadow-xl space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
            <div className="flex items-center gap-2">
              <TrendingUp className="h-4 w-4 text-cyan-400" />
              <h3 className="text-sm font-semibold text-slate-200">Daily Publishing & Rejection Volume</h3>
            </div>
            <span className="text-[11px] font-mono text-slate-400">Past 7 Days</span>
          </div>

          <div className="h-48 flex items-end justify-between gap-3 pt-6 px-2">
            {daily.map((d: any, idx: number) => {
              const maxVal = 5;
              const pubHeight = Math.min(100, Math.max(15, (d.published / maxVal) * 100));
              const rejHeight = Math.min(100, Math.max(10, (d.rejected / maxVal) * 100));

              return (
                <div key={idx} className="flex-1 flex flex-col items-center gap-2 h-full justify-end">
                  <div className="w-full flex items-end justify-center gap-1 h-36">
                    {/* Published Bar */}
                    <div
                      style={{ height: `${pubHeight}%` }}
                      className="w-1/2 rounded-t-md bg-gradient-to-t from-cyan-600 to-cyan-400 transition-all hover:brightness-125"
                      title={`${d.date}: ${d.published} Published`}
                    ></div>
                    {/* Rejected Bar */}
                    <div
                      style={{ height: `${rejHeight}%` }}
                      className="w-1/2 rounded-t-md bg-gradient-to-t from-amber-600 to-amber-400 transition-all hover:brightness-125"
                      title={`${d.date}: ${d.rejected} Rejected`}
                    ></div>
                  </div>
                  <span className="text-[10px] text-slate-400 font-mono">{d.date}</span>
                </div>
              );
            })}
          </div>

          <div className="flex items-center justify-center gap-6 pt-2 border-t border-slate-800/40 text-xs">
            <div className="flex items-center gap-1.5">
              <span className="h-3 w-3 rounded-sm bg-cyan-400"></span>
              <span className="text-slate-300">Published Posts</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="h-3 w-3 rounded-sm bg-amber-400"></span>
              <span className="text-slate-300">Rejected Topics</span>
            </div>
          </div>
        </div>

        {/* Topic Category Distribution */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 backdrop-blur-xl shadow-xl space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
            <div className="flex items-center gap-2">
              <PieChart className="h-4 w-4 text-purple-400" />
              <h3 className="text-sm font-semibold text-slate-200">Topic Categorization Breakdown</h3>
            </div>
            <span className="text-[11px] font-mono text-slate-400">Cognitive Focus</span>
          </div>

          <div className="space-y-4 pt-2">
            {categories.map((cat: any, cIdx: number) => {
              const count = cat.count || 1;
              const pct = Math.min(100, count * 25);
              return (
                <div key={cIdx} className="space-y-1.5">
                  <div className="flex justify-between text-xs">
                    <span className="font-medium text-slate-300">{cat.category}</span>
                    <span className="font-mono text-cyan-400">{count} posts</span>
                  </div>
                  <div className="h-2 w-full overflow-hidden rounded-full bg-slate-800">
                    <div
                      style={{ width: `${pct}%` }}
                      className="h-full rounded-full bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-500 transition-all duration-500"
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};
