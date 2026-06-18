"use client";

import { useState } from "react";
import { AlertTriangle, Home, IndianRupee, MapPin } from "lucide-react";
import Link from "next/link";

export default function DistressPropertiesPage() {
  const [properties] = useState([
    {
      id: "1",
      title: "Omaxe Residency Unit 4B",
      location: "Gomti Nagar Extension, Lucknow",
      type: "Bank Auction",
      market_value: 8500000,
      reserve_price: 6200000,
      discount: 27,
      auction_date: "2026-07-15",
    },
    {
      id: "2",
      title: "Commercial Plot, Phase 2",
      location: "Shaheed Path Corridor, Lucknow",
      type: "Distress Sale",
      market_value: 12000000,
      reserve_price: 9500000,
      discount: 21,
      auction_date: "Immediate",
    }
  ]);

  return (
    <div className="max-w-6xl mx-auto p-4 md:p-8">
      <div className="mb-8 border-b border-gray-200 pb-6">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 bg-red-100 rounded-lg text-red-600">
            <AlertTriangle className="w-6 h-6" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900">Distress Properties</h1>
        </div>
        <p className="text-gray-600">Discover undervalued properties, bank auctions, and distress sales near high-growth infrastructure zones.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {properties.map(prop => (
          <div key={prop.id} className="bg-white border border-gray-200 rounded-xl overflow-hidden hover:shadow-md transition-shadow">
            <div className="p-5 border-b border-gray-100 flex justify-between items-start">
              <div>
                <span className="inline-block px-2.5 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800 mb-3">
                  {prop.type}
                </span>
                <h3 className="text-lg font-bold text-gray-900 mb-1">{prop.title}</h3>
                <div className="flex items-center gap-1.5 text-sm text-gray-500">
                  <MapPin className="w-4 h-4" /> {prop.location}
                </div>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-emerald-600">-{prop.discount}%</div>
                <div className="text-xs text-gray-500 uppercase">Below Market</div>
              </div>
            </div>
            
            <div className="p-5 bg-gray-50 grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-500 mb-1">Reserve Price</p>
                <p className="font-bold text-gray-900 flex items-center">
                  <IndianRupee className="w-4 h-4 mr-0.5" /> {(prop.reserve_price / 100000).toFixed(1)} Lakhs
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500 mb-1">Est. Market Value</p>
                <p className="font-medium text-gray-400 line-through flex items-center">
                  <IndianRupee className="w-4 h-4 mr-0.5" /> {(prop.market_value / 100000).toFixed(1)} Lakhs
                </p>
              </div>
            </div>
            
            <div className="p-4 flex justify-between items-center border-t border-gray-100">
              <span className="text-sm text-gray-600">Date: <strong>{prop.auction_date}</strong></span>
              <button className="px-4 py-2 bg-gray-900 text-white text-sm font-medium rounded-lg hover:bg-gray-800 transition-colors">
                View Details
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
