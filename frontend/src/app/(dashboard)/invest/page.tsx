"use client";

import { useState } from "react";
import { Bot, ChevronRight, CheckCircle2, TrendingUp } from "lucide-react";
import Link from "next/link";

export default function InvestmentAssistantPage() {
  const [step, setStep] = useState(1);
  const [budget, setBudget] = useState(50);
  const [risk, setRisk] = useState("moderate");
  const [loading, setLoading] = useState(false);
  const [recommendation, setRecommendation] = useState<any>(null);

  const generateStrategy = () => {
    setLoading(true);
    // Simulate LangGraph Agent call
    setTimeout(() => {
      setRecommendation({
        strategy: "Focus on commercial plots along the newly announced East-West Metro corridor.",
        target_areas: ["Vasant Kunj", "Aminabad"],
        expected_roi: "18-22% p.a.",
        rationale: "Your moderate risk profile and 50L budget aligns perfectly with pre-construction commercial plots near upcoming metro stations, which historically appreciate significantly once construction breaks ground."
      });
      setLoading(false);
      setStep(3);
    }, 2000);
  };

  return (
    <div className="max-w-4xl mx-auto p-4 md:p-8">
      <div className="text-center mb-10">
        <div className="inline-flex items-center justify-center p-3 bg-emerald-100 rounded-2xl text-emerald-600 mb-4">
          <Bot className="w-10 h-10" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 mb-3">AI Investment Assistant</h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">Tell us your investment goals, and our LangGraph agents will analyze all upcoming infrastructure to generate a personalized strategy.</p>
      </div>

      <div className="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
        {step === 1 && (
          <div className="p-8">
            <h2 className="text-xl font-bold mb-6">What is your investment budget?</h2>
            <div className="mb-8">
              <input 
                type="range" 
                min="10" 
                max="500" 
                value={budget} 
                onChange={(e) => setBudget(Number(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-emerald-600"
              />
              <div className="mt-4 text-center text-3xl font-bold text-emerald-600">₹{budget} Lakhs</div>
            </div>
            <button 
              onClick={() => setStep(2)}
              className="w-full py-4 bg-emerald-600 text-white rounded-xl font-bold text-lg hover:bg-emerald-700 transition-colors flex items-center justify-center"
            >
              Next Step <ChevronRight className="w-5 h-5 ml-2" />
            </button>
          </div>
        )}

        {step === 2 && (
          <div className="p-8">
            <h2 className="text-xl font-bold mb-6">What is your risk tolerance?</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
              {['low', 'moderate', 'high'].map((r) => (
                <button
                  key={r}
                  onClick={() => setRisk(r)}
                  className={`p-4 rounded-xl border-2 text-center capitalize transition-all ${risk === r ? 'border-emerald-600 bg-emerald-50 text-emerald-700' : 'border-gray-200 hover:border-emerald-200'}`}
                >
                  {r} Risk
                </button>
              ))}
            </div>
            <button 
              onClick={generateStrategy}
              disabled={loading}
              className="w-full py-4 bg-gray-900 text-white rounded-xl font-bold text-lg hover:bg-gray-800 transition-colors flex items-center justify-center disabled:opacity-70"
            >
              {loading ? "Agents are analyzing..." : "Generate AI Strategy"}
            </button>
          </div>
        )}

        {step === 3 && recommendation && (
          <div className="p-8">
            <div className="flex items-center gap-3 mb-6 text-emerald-600">
              <CheckCircle2 className="w-8 h-8" />
              <h2 className="text-2xl font-bold">Your Custom AI Strategy</h2>
            </div>
            
            <div className="bg-gray-50 rounded-xl p-6 mb-6 border border-gray-100">
              <p className="text-lg text-gray-800 leading-relaxed mb-6">
                "{recommendation.strategy}"
              </p>
              
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <p className="text-sm text-gray-500 uppercase tracking-wider mb-2">Target Areas</p>
                  <div className="flex gap-2">
                    {recommendation.target_areas.map((a: string) => (
                      <span key={a} className="px-3 py-1 bg-white border border-gray-200 rounded-lg text-sm font-medium">{a}</span>
                    ))}
                  </div>
                </div>
                <div>
                  <p className="text-sm text-gray-500 uppercase tracking-wider mb-2">Expected ROI</p>
                  <p className="text-xl font-bold text-emerald-600 flex items-center gap-1">
                    <TrendingUp className="w-5 h-5" /> {recommendation.expected_roi}
                  </p>
                </div>
              </div>
            </div>

            <div className="mb-8">
              <h3 className="font-bold text-gray-900 mb-2">Agent Rationale</h3>
              <p className="text-gray-600">{recommendation.rationale}</p>
            </div>

            <div className="flex gap-4">
              <button onClick={() => setStep(1)} className="px-6 py-3 border border-gray-300 rounded-xl font-medium hover:bg-gray-50 transition-colors">
                Recalculate
              </button>
              <Link href="/map" className="flex-1 text-center py-3 bg-emerald-600 text-white rounded-xl font-bold hover:bg-emerald-700 transition-colors">
                View Target Areas on Map
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
