"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Compass, TrendingUp, MapPin, Search } from "lucide-react";
import { getAreas } from "@/lib/api";

export default function AreaIntelligencePage() {
  const [areas, setAreas] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadAreas() {
      try {
        const data = await getAreas({ city: "Lucknow" });
        const mapped = (data.items || []).map((a: any) => ({
          id: a.slug,
          name: a.name,
          city: a.city,
          score: Math.round(a.growth_rate_pct * 4 + 10),
          growth: a.growth_rate_pct,
          price: a.avg_price_sqft
        }));
        setAreas(mapped);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadAreas();
  }, []);

  return (
    <div className="max-w-6xl mx-auto p-4 md:p-8">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 bg-emerald-100 rounded-lg text-emerald-600">
            <Compass className="w-6 h-6" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900">Area Intelligence</h1>
        </div>
        <p className="text-gray-600">Discover high-potential investment zones based on our proprietary Opportunity Score.</p>
      </div>

      <div className="mb-8 relative max-w-2xl">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5" />
        <input 
          type="text" 
          placeholder="Search for a locality or district..." 
          className="w-full pl-12 pr-4 py-4 bg-white border border-gray-300 rounded-xl shadow-sm focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
        />
      </div>

      {loading ? (
        <div className="text-center py-12 text-gray-500">Calculating opportunity scores...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {areas.map((area) => (
            <Link key={area.id} href={`/area/${area.id}`} className="block group">
              <div className="bg-white border border-gray-200 rounded-xl p-6 hover:shadow-lg transition-all hover:border-emerald-200 relative overflow-hidden">
                <div className="absolute top-0 right-0 p-6 opacity-5 group-hover:opacity-10 transition-opacity">
                  <TrendingUp className="w-24 h-24" />
                </div>
                
                <h3 className="text-xl font-bold text-gray-900 mb-1">{area.name}</h3>
                <div className="flex items-center gap-1.5 text-sm text-gray-500 mb-6">
                  <MapPin className="w-4 h-4" /> {area.city}
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Opportunity Score</p>
                    <div className="flex items-end gap-1">
                      <span className="text-3xl font-bold text-emerald-600">{area.score}</span>
                      <span className="text-sm font-medium text-gray-400 mb-1">/100</span>
                    </div>
                  </div>
                  
                  <div>
                    <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Growth Rate</p>
                    <div className="flex items-end gap-1">
                      <span className="text-2xl font-bold text-gray-900">+{area.growth}%</span>
                      <span className="text-xs font-medium text-gray-400 mb-1">p.a.</span>
                    </div>
                  </div>
                </div>
                
                <div className="mt-6 pt-4 border-t border-gray-100 flex justify-between items-center text-sm">
                  <span className="text-gray-500">Avg. ₹{area.price}/sqft</span>
                  <span className="text-emerald-600 font-medium group-hover:underline">View Intelligence →</span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
