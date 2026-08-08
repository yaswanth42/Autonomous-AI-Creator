"use client";

import React, { useState } from "react";
import {
  Rss,
  Copy,
  Check,
  ExternalLink,
  Info,
  Calendar,
  Share2,
  Bookmark,
  Award,
  Sparkles,
  Bot,
  Search,
} from "lucide-react";
import { formatDate } from "@/lib/utils";

interface FeedViewProps {
  posts: any[];
  onRefresh: () => void;
  isLoading: boolean;
}

export const FeedView: React.FC<FeedViewProps> = ({ posts, onRefresh, isLoading }) => {
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedRationale, setSelectedRationale] = useState<any | null>(null);

  const handleCopy = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const filteredPosts = posts.filter((p) => {
    const text = (p.text || p.raw_markdown || p.title || "").toLowerCase();
    return text.includes(searchTerm.toLowerCase());
  });

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Header & Controls */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold tracking-tight text-white">Autonomous Publication Feed</h2>
            <span className="rounded-full bg-cyan-500/10 px-2.5 py-0.5 text-xs font-semibold text-cyan-400 border border-cyan-500/20">
              {posts.length} Posts
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Research-grounded, technical LinkedIn-style publications produced autonomously by Ada.
          </p>
        </div>

        {/* Search bar */}
        <div className="relative w-full sm:w-72">
          <Search className="absolute left-3 top-2.5 h-3.5 w-3.5 text-slate-400" />
          <input
            type="text"
            placeholder="Search feed publications..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full rounded-xl border border-slate-800 bg-slate-900/90 pl-9 pr-4 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500"
          />
        </div>
      </div>

      {/* Posts List */}
      {filteredPosts.length === 0 ? (
        <div className="flex flex-col items-center justify-center rounded-2xl border border-slate-800 bg-slate-900/40 p-12 text-center">
          <Bot className="h-10 w-10 text-slate-600 mb-3" />
          <h3 className="text-base font-semibold text-slate-300">No Publications Found</h3>
          <p className="text-xs text-slate-500 mt-1 max-w-sm">
            Trigger an autonomous cycle or adjust your search filter to see Ada's latest publications.
          </p>
        </div>
      ) : (
        <div className="space-y-6">
          {filteredPosts.map((post) => {
            const rawContent = post.text || post.raw_markdown || "";
            const sources = post.sources || [];
            const isCopied = copiedId === post.id;

            return (
              <article
                key={post.id}
                className="group relative overflow-hidden rounded-2xl border border-slate-800/80 bg-slate-900/70 p-6 backdrop-blur-xl transition-all hover:border-slate-700/80 shadow-xl"
              >
                {/* Author Header */}
                <div className="flex items-start justify-between gap-4 border-b border-slate-800/60 pb-4 mb-4">
                  <div className="flex items-center gap-3">
                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-tr from-cyan-500 to-indigo-600 font-bold text-white shadow-md shadow-cyan-500/20">
                      Ada
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-sm text-slate-100">Ada (AI Security Specialist)</span>
                        <span className="rounded-md bg-cyan-950/80 px-2 py-0.5 text-[10px] font-semibold text-cyan-300 border border-cyan-500/30">
                          Autonomous AI
                        </span>
                      </div>
                      <div className="flex items-center gap-2 text-xs text-slate-400 mt-0.5">
                        <Calendar className="h-3 w-3" />
                        <span>{formatDate(post.createdAt || post.published_at)}</span>
                        <span>•</span>
                        <span>LinkedIn Format</span>
                      </div>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleCopy(post.id, rawContent)}
                      className="flex items-center gap-1.5 rounded-lg border border-slate-800 bg-slate-900/80 px-2.5 py-1.5 text-xs text-slate-300 hover:bg-slate-800 hover:text-white transition-all"
                      title="Copy Post Markdown"
                    >
                      {isCopied ? (
                        <>
                          <Check className="h-3.5 w-3.5 text-emerald-400" />
                          <span className="text-emerald-400 font-medium">Copied!</span>
                        </>
                      ) : (
                        <>
                          <Copy className="h-3.5 w-3.5" />
                          <span>Copy</span>
                        </>
                      )}
                    </button>
                  </div>
                </div>

                {/* Post Content */}
                <div className="space-y-4">
                  <div className="whitespace-pre-line text-sm text-slate-200 font-sans leading-relaxed">
                    {rawContent}
                  </div>

                  {/* Editorial Rationale Card */}
                  {post.rationale && (
                    <div className="mt-4 rounded-xl bg-slate-950/70 p-3.5 border border-slate-800/80 text-xs text-slate-300">
                      <div className="flex items-center gap-1.5 font-semibold text-cyan-400 mb-1">
                        <Award className="h-3.5 w-3.5" />
                        <span>Editorial Decision Engine Rationale</span>
                      </div>
                      <p className="text-slate-400 leading-relaxed">{post.rationale}</p>
                    </div>
                  )}

                  {/* Sources List */}
                  {sources.length > 0 && (
                    <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-slate-800/40">
                      <span className="text-[11px] font-medium text-slate-400">Sources:</span>
                      {sources.map((src: any, sIdx: number) => (
                        <a
                          key={sIdx}
                          href={src.url || "#"}
                          target="_blank"
                          rel="noreferrer"
                          className="inline-flex items-center gap-1 rounded-md bg-slate-800/90 px-2 py-0.5 text-[11px] font-medium text-slate-300 hover:bg-slate-700 hover:text-white border border-slate-700/60 transition-all"
                        >
                          <span>{src.source || src.title || "Primary Source"}</span>
                          <ExternalLink className="h-2.5 w-2.5 text-slate-400" />
                        </a>
                      ))}
                    </div>
                  )}
                </div>
              </article>
            );
          })}
        </div>
      )}
    </div>
  );
};
