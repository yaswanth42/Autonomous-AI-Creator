"use client";

import React from "react";
import {
  Sparkles,
  Bot,
  Rss,
  Brain,
  ShieldAlert,
  Globe,
  BarChart3,
  Terminal,
  Play,
  Loader2,
} from "lucide-react";

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  onTriggerCycle: () => void;
  isTriggering: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  onTriggerCycle,
  isTriggering,
}) => {
  const navItems = [
    { id: "overview", label: "Overview", icon: Sparkles },
    { id: "feed", label: "Feed", icon: Rss },
    { id: "agent", label: "Agent Status", icon: Bot },
    { id: "memory", label: "Breeth Memory", icon: Brain },
    { id: "rejected", label: "Rejected Topics", icon: ShieldAlert },
    { id: "sources", label: "Sources", icon: Globe },
    { id: "analytics", label: "Analytics", icon: BarChart3 },
    { id: "ai-usage", label: "AI Tracker", icon: Terminal },
  ];

  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6">
        {/* Brand Logo */}
        <div
          className="flex items-center gap-3 cursor-pointer"
          onClick={() => setActiveTab("overview")}
        >
          <div className="relative flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-cyan-500 to-indigo-600 shadow-lg shadow-cyan-500/25 ring-1 ring-white/20">
            <Bot className="h-5 w-5 text-white" />
            <span className="absolute -top-1 -right-1 flex h-3 w-3">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-cyan-400 opacity-75"></span>
              <span className="relative inline-flex h-3 w-3 rounded-full bg-cyan-500"></span>
            </span>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-lg font-bold tracking-tight text-white">
                AutoPersona<span className="text-cyan-400">.AI</span>
              </span>
              <span className="rounded-md bg-cyan-950/80 px-2 py-0.5 text-[10px] font-semibold text-cyan-300 border border-cyan-500/30">
                Ada • AI Security
              </span>
            </div>
            <p className="text-xs text-slate-400">Autonomous Technology Persona</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="hidden lg:flex items-center gap-1 rounded-xl bg-slate-900/90 p-1 border border-slate-800">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center gap-2 rounded-lg px-3 py-1.5 text-xs font-medium transition-all ${
                  isActive
                    ? "bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-md shadow-cyan-500/20"
                    : "text-slate-400 hover:bg-slate-800/60 hover:text-slate-200"
                }`}
              >
                <Icon className="h-3.5 w-3.5" />
                {item.label}
              </button>
            );
          })}
        </nav>

        {/* Trigger Button */}
        <div className="flex items-center gap-2">
          <button
            onClick={onTriggerCycle}
            disabled={isTriggering}
            className="relative flex items-center gap-2 rounded-xl bg-gradient-to-r from-cyan-500 via-blue-500 to-indigo-600 px-4 py-2 text-xs font-semibold text-white shadow-lg shadow-cyan-500/20 transition-all hover:scale-[1.02] hover:shadow-cyan-500/40 active:scale-95 disabled:opacity-50"
          >
            {isTriggering ? (
              <>
                <Loader2 className="h-3.5 w-3.5 animate-spin" />
                <span>Running Cycle...</span>
              </>
            ) : (
              <>
                <Play className="h-3.5 w-3.5 fill-current" />
                <span>Trigger Cycle</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Mobile Navigation */}
      <div className="flex lg:hidden overflow-x-auto border-t border-slate-800/60 bg-slate-900/60 px-4 py-2 gap-1 scrollbar-none">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex items-center gap-1.5 whitespace-nowrap rounded-lg px-2.5 py-1 text-xs font-medium ${
                isActive
                  ? "bg-cyan-500/20 text-cyan-400 border border-cyan-500/30"
                  : "text-slate-400"
              }`}
            >
              <Icon className="h-3 w-3" />
              {item.label}
            </button>
          );
        })}
      </div>
    </header>
  );
};
