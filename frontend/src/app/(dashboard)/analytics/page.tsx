"use client";

import { BarChart3, Users, Zap, TrendingUp } from "lucide-react";

export default function AnalyticsDashboard() {
  return (
    <div className="max-w-6xl mx-auto p-4 md:p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Platform Analytics</h1>
        <p className="text-gray-600">Overview of system health, active users, and LangGraph agent performance.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center gap-3 text-gray-500 mb-4">
            <Users className="w-5 h-5 text-indigo-500" />
            <h3 className="font-medium">Daily Active Users</h3>
          </div>
          <p className="text-3xl font-bold text-gray-900">1,284</p>
          <p className="text-sm text-emerald-600 flex items-center mt-2"><TrendingUp className="w-4 h-4 mr-1" /> +12% this week</p>
        </div>

        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center gap-3 text-gray-500 mb-4">
            <Zap className="w-5 h-5 text-emerald-500" />
            <h3 className="font-medium">AI Queries</h3>
          </div>
          <p className="text-3xl font-bold text-gray-900">8,592</p>
          <p className="text-sm text-gray-500 mt-2">Llama 3.3 70B via Groq</p>
        </div>

        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center gap-3 text-gray-500 mb-4">
            <BarChart3 className="w-5 h-5 text-blue-500" />
            <h3 className="font-medium">Avg Agent Latency</h3>
          </div>
          <p className="text-3xl font-bold text-gray-900">840ms</p>
          <p className="text-sm text-emerald-600 mt-2">Optimal</p>
        </div>

        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center gap-3 text-gray-500 mb-4">
            <TrendingUp className="w-5 h-5 text-rose-500" />
            <h3 className="font-medium">Projects Ingested</h3>
          </div>
          <p className="text-3xl font-bold text-gray-900">156</p>
          <p className="text-sm text-gray-500 mt-2">Across 3 Cities</p>
        </div>
      </div>

      <div className="bg-white p-8 rounded-xl border border-gray-200 shadow-sm">
        <h2 className="text-xl font-bold mb-4">System Observability</h2>
        <p className="text-gray-600 mb-6">
          Detailed metrics are available via our dedicated observability stack.
        </p>
        <div className="flex gap-4">
          <a href="http://localhost:3001" target="_blank" className="px-6 py-3 bg-gray-900 text-white rounded-lg font-medium hover:bg-gray-800">
            Open Grafana Dashboard
          </a>
          <a href="http://localhost:6006" target="_blank" className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50">
            Open Arize Phoenix (LLM Traces)
          </a>
        </div>
      </div>
    </div>
  );
}
