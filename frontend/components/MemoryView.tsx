"use client";

import React, { useState } from "react";
import {
  Brain,
  Search,
  Layers,
  Sparkles,
  Tag,
  Clock,
  CheckCircle2,
  Database,
  ArrowUpRight,
  Filter,
} from "lucide-react";
import { formatDate } from "@/lib/utils";

interface MemoryViewProps {
  memories: any[];
  onQueryMemory: (query: string) => Promise<any[]>;
}

export const MemoryView: React.FC<MemoryViewProps> = ({ memories, onQueryMemory }) => {
  const [activeCategory, setActiveCategory] = useState("ALL");
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<any[] | null>(null);
  const [isSearching, setIsSearching] = useState(false);

  const categories = ["ALL", "POST", "REJECTED", "PREFERENCE", "STYLE", "REASONING"];

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) {
      setSearchResults(null);
      return;
    }
    setIsSearching(true);
    try {
      const results = await onQueryMemory(searchQuery);
      setSearchResults(results);
    } catch (err) {
      console.error("Memory search error:", err);
    } finally {
      setIsSearching(false);
    }
  };

  const displayedMemories = searchResults !== null
    ? searchResults
    : memories.filter((m) => {
        if (activeCategory === "ALL") return true;
        return m.category?.toUpperCase() === activeCategory.toUpperCase() ||
               m.memory_type?.toUpperCase() === activeCategory.toUpperCase();
      });

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold tracking-tight text-white">Breeth Memory Engine</h2>
            <span className="rounded-full bg-purple-500/10 px-2.5 py-0.5 text-xs font-semibold text-purple-400 border border-purple-500/20">
              {memories.length} Cognitive Nodes
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Persistent cognitive memory store powering semantic deduplication, voice continuity, and editorial memory.
          </p>
        </div>
      </div>

      {/* Semantic Query Console */}
      <div className="rounded-2xl border border-purple-500/20 bg-gradient-to-b from-purple-950/20 via-slate-900/60 to-slate-950/80 p-6 backdrop-blur-xl shadow-xl space-y-4">
        <div className="flex items-center gap-2 text-xs font-mono uppercase tracking-wider text-purple-400">
          <Brain className="h-4 w-4" />
          <span>Semantic Vector Search Tester</span>
        </div>

        <form onSubmit={handleSearch} className="flex gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-3 h-4 w-4 text-slate-400" />
            <input
              type="text"
              placeholder="Query Breeth Memory (e.g. 'MCP sandbox escape vulnerability', 'clickbait policy')..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full rounded-xl border border-slate-800 bg-slate-900/90 pl-10 pr-4 py-2.5 text-xs text-slate-200 placeholder-slate-500 focus:border-purple-500 focus:outline-none focus:ring-1 focus:ring-purple-500"
            />
          </div>
          <button
            type="submit"
            disabled={isSearching}
            className="rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 px-5 py-2.5 text-xs font-semibold text-white shadow-lg shadow-purple-500/20 hover:scale-[1.02] transition-all disabled:opacity-50"
          >
            {isSearching ? "Searching..." : "Query Memory"}
          </button>
          {searchResults !== null && (
            <button
              type="button"
              onClick={() => {
                setSearchResults(null);
                setSearchQuery("");
              }}
              className="rounded-xl bg-slate-800 px-4 py-2.5 text-xs font-medium text-slate-300 hover:bg-slate-700 transition-all"
            >
              Reset
            </button>
          )}
        </form>
      </div>

      {/* Category Filter Tabs */}
      <div className="flex overflow-x-auto gap-2 border-b border-slate-800/80 pb-2 scrollbar-none">
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => {
              setActiveCategory(cat);
              setSearchResults(null);
            }}
            className={`whitespace-nowrap rounded-lg px-3 py-1.5 text-xs font-medium transition-all ${
              activeCategory === cat && searchResults === null
                ? "bg-purple-500/20 text-purple-300 border border-purple-500/40"
                : "text-slate-400 hover:bg-slate-800/60 hover:text-slate-200"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Memory Nodes Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {displayedMemories.map((mem) => {
          const importance = mem.importance || 1.0;
          const similarity = mem.similarity !== undefined ? mem.similarity : null;

          return (
            <div
              key={mem.id}
              className="relative overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/70 p-5 backdrop-blur-xl space-y-3 transition-all hover:border-purple-500/30 hover:translate-y-[-2px] shadow-lg"
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-center gap-2">
                  <span className="rounded-md bg-purple-950/80 px-2 py-0.5 text-[10px] font-mono font-semibold text-purple-300 border border-purple-500/30 uppercase">
                    {mem.category || mem.memory_type || "NODE"}
                  </span>
                  {similarity !== null && (
                    <span className="rounded-md bg-emerald-950/80 px-2 py-0.5 text-[10px] font-mono font-semibold text-emerald-300 border border-emerald-500/30">
                      Sim: {(similarity * 100).toFixed(1)}%
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-1.5 text-[11px] text-slate-500 font-mono">
                  <Clock className="h-3 w-3" />
                  <span>{formatDate(mem.created_at || mem.last_accessed_at)}</span>
                </div>
              </div>

              <p className="text-xs text-slate-200 font-sans leading-relaxed whitespace-pre-line">
                {mem.content}
              </p>

              <div className="flex items-center justify-between pt-3 border-t border-slate-800/60 text-[11px] text-slate-400">
                <div className="flex items-center gap-1">
                  <Tag className="h-3 w-3 text-purple-400" />
                  <span>Weight: {importance.toFixed(2)}</span>
                </div>
                <div className="font-mono text-slate-500 text-[10px]">
                  ID: {mem.id?.slice(0, 8)}...
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
