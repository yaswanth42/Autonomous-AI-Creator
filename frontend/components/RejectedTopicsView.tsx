"use client";

import React from "react";
import {
  ShieldAlert,
  AlertTriangle,
  XCircle,
  ExternalLink,
  Calendar,
  BarChart2,
  Filter,
} from "lucide-react";
import { formatDate } from "@/lib/utils";

interface RejectedTopicsViewProps {
  rejectedTopics: any[];
}

export const RejectedTopicsView: React.FC<RejectedTopicsViewProps> = ({ rejectedTopics }) => {
  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold tracking-tight text-white">Editorial Quality Gate & Rejections</h2>
            <span className="rounded-full bg-amber-500/10 px-2.5 py-0.5 text-xs font-semibold text-amber-400 border border-amber-500/20">
              {rejectedTopics.length} Filtered Out
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Topics evaluated by the 7-factor editorial decision engine that failed the 7.0/10 quality threshold.
          </p>
        </div>
      </div>

      {rejectedTopics.length === 0 ? (
        <div className="flex flex-col items-center justify-center rounded-2xl border border-slate-800 bg-slate-900/40 p-12 text-center">
          <ShieldAlert className="h-10 w-10 text-slate-600 mb-3" />
          <h3 className="text-base font-semibold text-slate-300">No Rejected Topics</h3>
          <p className="text-xs text-slate-500 mt-1 max-w-sm">
            All evaluated topics have met or exceeded the 7.0 threshold.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {rejectedTopics.map((topic) => {
            const scoreBreakdown = topic.score_breakdown || {};
            const totalScore = topic.total_score || 0;

            return (
              <div
                key={topic.id}
                className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/70 p-6 backdrop-blur-xl space-y-4 transition-all hover:border-amber-500/30 shadow-xl"
              >
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-slate-800/60 pb-3">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="inline-flex items-center gap-1 rounded-md bg-red-950/80 px-2 py-0.5 text-[10px] font-semibold text-red-400 border border-red-500/30">
                        <XCircle className="h-3 w-3" />
                        REJECTED
                      </span>
                      <span className="text-xs text-slate-400 font-mono">
                        {formatDate(topic.created_at)}
                      </span>
                    </div>
                    <h3 className="text-base font-bold text-white">{topic.title}</h3>
                  </div>

                  <div className="flex items-center gap-3">
                    <div className="text-right">
                      <div className="text-[10px] uppercase font-mono text-slate-400">Total Score</div>
                      <div className="text-lg font-extrabold text-amber-400 font-mono">
                        {totalScore.toFixed(1)} <span className="text-xs text-slate-500 font-normal">/ 10</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Rejection Reason */}
                <div className="rounded-xl bg-slate-950/80 p-3.5 border border-slate-800/80 text-xs text-slate-300">
                  <div className="flex items-center gap-1.5 font-semibold text-amber-400 mb-1">
                    <AlertTriangle className="h-3.5 w-3.5" />
                    <span>Rejection Rationale</span>
                  </div>
                  <p className="text-slate-400 leading-relaxed">{topic.reason}</p>
                </div>

                {/* 7-Factor Score Breakdown */}
                <div className="space-y-2">
                  <span className="text-[11px] font-mono uppercase text-slate-400 flex items-center gap-1">
                    <BarChart2 className="h-3 w-3 text-cyan-400" />
                    7-Factor Score Breakdown
                  </span>
                  <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2">
                    {[
                      { name: "Novelty", val: topic.novelty ?? scoreBreakdown.novelty ?? 5.0 },
                      { name: "Importance", val: topic.importance ?? scoreBreakdown.importance ?? 6.0 },
                      { name: "Trust", val: topic.trustworthiness ?? scoreBreakdown.trustworthiness ?? 6.0 },
                      { name: "Trending", val: topic.trending_score ?? scoreBreakdown.trending_score ?? 6.0 },
                      { name: "Tech Value", val: topic.technical_value ?? scoreBreakdown.technical_value ?? 5.0 },
                      { name: "Community", val: topic.community_impact ?? scoreBreakdown.community_impact ?? 5.0 },
                      { name: "Dup Penalty", val: topic.duplicate_penalty ?? scoreBreakdown.duplicate_penalty ?? 0.0, isPenalty: true },
                    ].map((factor, fIdx) => (
                      <div
                        key={fIdx}
                        className="rounded-lg bg-slate-950/50 p-2 border border-slate-800 text-center"
                      >
                        <div className="text-[10px] text-slate-400">{factor.name}</div>
                        <div
                          className={`text-xs font-bold font-mono mt-0.5 ${
                            factor.isPenalty
                              ? "text-red-400"
                              : Number(factor.val) >= 7.0
                              ? "text-emerald-400"
                              : "text-amber-400"
                          }`}
                        >
                          {Number(factor.val).toFixed(1)}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Source link */}
                {topic.url && (
                  <div className="flex justify-end pt-2">
                    <a
                      href={topic.url}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center gap-1 text-[11px] text-slate-400 hover:text-slate-200"
                    >
                      <span>View source: {topic.source || "External Link"}</span>
                      <ExternalLink className="h-3 w-3" />
                    </a>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
