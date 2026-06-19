"use client";

import { useState, useEffect } from "react";
import { AlertTriangle, Home, IndianRupee, MapPin, Sparkles, RefreshCw, ShieldCheck, X, Building } from "lucide-react";
import Link from "next/link";
import { getDistressProperties, scanDistressProperties } from "@/lib/api";
import { useCity } from "@/components/providers/CityProvider";

export default function DistressPropertiesPage() {
  const [properties, setProperties] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [scanning, setScanning] = useState(false);
  const [scanStatus, setScanStatus] = useState("");
  const [selectedProperty, setSelectedProperty] = useState<any | null>(null);
  const { city } = useCity();

  async function loadProperties() {
    setLoading(true);
    try {
      const data = await getDistressProperties({ city });
      setProperties(data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadProperties();
  }, [city]);

  const handleScan = async () => {
    if (scanning) return;
    setScanning(true);
    setScanStatus("Querying MSTC, IBAPI & eBkray search portals...");

    // Setup progressive status updates
    const statusIntervals = [
      { delay: 2000, msg: "Extracting auction records and listing metadata..." },
      { delay: 4000, msg: "Running Verification Agent to validate reserve prices and locations..." },
      { delay: 7000, msg: "Matching verified listings against nearby high-growth infrastructure zones..." },
      { delay: 10000, msg: "Finalizing database entries and compiling results..." }
    ];

    const timers = statusIntervals.map(step => 
      setTimeout(() => setScanStatus(step.msg), step.delay)
    );

    try {
      const updatedListings = await scanDistressProperties(city);
      setProperties(updatedListings || []);
    } catch (err) {
      console.error("Scan failed:", err);
    } finally {
      timers.forEach(t => clearTimeout(t));
      setScanning(false);
      setScanStatus("");
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-4 md:p-8">
      <div className="mb-8 border-b border-gray-200 pb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-red-100 rounded-lg text-red-600">
              <AlertTriangle className="w-6 h-6" />
            </div>
            <h1 className="text-3xl font-bold text-gray-900">Distress Properties</h1>
          </div>
          <p className="text-gray-600">Discover undervalued properties, bank auctions, and distress sales near high-growth infrastructure zones.</p>
        </div>
        <button
          onClick={handleScan}
          disabled={scanning}
          className="flex items-center gap-2 px-5 py-3 bg-red-600 text-white rounded-xl shadow-md hover:bg-red-700 hover:shadow-lg disabled:bg-gray-400 disabled:shadow-none transition-all font-semibold text-sm self-start md:self-center"
        >
          {scanning ? (
            <>
              <RefreshCw className="w-4 h-4 animate-spin" />
              <span>Scanning...</span>
            </>
          ) : (
            <>
              <Sparkles className="w-4 h-4" />
              <span>Scan & Verify Live Listings</span>
            </>
          )}
        </button>
      </div>

      {scanning && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl flex items-center gap-3 animate-pulse">
          <RefreshCw className="w-5 h-5 text-red-600 animate-spin" />
          <div className="flex-1">
            <h4 className="font-bold text-red-900 text-sm">AI Search & Verification Agent Active</h4>
            <p className="text-red-700 text-xs mt-0.5">{scanStatus}</p>
          </div>
        </div>
      )}

      {loading ? (
        <div className="text-center py-12 text-gray-500">Loading distress properties...</div>
      ) : properties.length === 0 ? (
        <div className="text-center py-12 text-gray-500">No distress properties found.</div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {properties.map((prop: any) => (
            <div key={prop.id} className="bg-white border border-gray-200 rounded-xl overflow-hidden hover:shadow-md transition-shadow">
              <div className="p-5 border-b border-gray-100 flex justify-between items-start">
                <div>
                  <span className="inline-block px-2.5 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800 mb-3">
                    {prop.property_type}
                  </span>
                  <h3 className="text-lg font-bold text-gray-900 mb-1">{prop.title}</h3>
                  <div className="flex items-center gap-1.5 text-sm text-gray-500">
                    <MapPin className="w-4 h-4" /> {prop.location}
                  </div>
                  {prop.backing_authority && (
                    <div className="flex items-center gap-1.5 mt-2.5 text-xs font-semibold text-indigo-700 bg-indigo-50 border border-indigo-100 rounded-lg px-2.5 py-1 w-fit shadow-sm">
                      <ShieldCheck className="w-3.5 h-3.5 text-indigo-600" />
                      <span>{prop.backing_authority}</span>
                    </div>
                  )}
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
                <button 
                  onClick={() => setSelectedProperty(prop)}
                  className="px-4 py-2 bg-gray-900 text-white text-sm font-medium rounded-lg hover:bg-gray-800 transition-colors"
                >
                  View Details
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Distress Property Details Modal */}
      {selectedProperty && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center p-4 z-50 transition-opacity">
          <div className="bg-white rounded-2xl max-w-lg w-full overflow-hidden shadow-2xl relative border border-gray-150 animate-in fade-in zoom-in duration-200">
            {/* Modal Header */}
            <div className="p-6 border-b border-gray-150 flex justify-between items-start">
              <div>
                <span className="inline-block px-2.5 py-1 rounded-full text-xs font-semibold bg-red-100 text-red-800 mb-2">
                  {selectedProperty.property_type}
                </span>
                <h2 className="text-xl font-bold text-gray-950">{selectedProperty.title}</h2>
              </div>
              <button 
                onClick={() => setSelectedProperty(null)}
                className="p-1 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            {/* Modal Body */}
            <div className="p-6 space-y-6">
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <MapPin className="w-4 h-4 text-gray-400" />
                  <span>{selectedProperty.location}</span>
                </div>
                
                {selectedProperty.backing_authority && (
                  <div className="flex items-center gap-2 text-sm text-indigo-700 bg-indigo-50 border border-indigo-100 rounded-lg px-3 py-1.5 w-fit shadow-sm">
                    <ShieldCheck className="w-4.5 h-4.5 text-indigo-600" />
                    <span>Backed by: <strong>{selectedProperty.backing_authority}</strong></span>
                  </div>
                )}
              </div>
              
              {/* Financial Section */}
              <div className="grid grid-cols-2 gap-4 bg-gray-50 p-4 rounded-xl border border-gray-100">
                <div>
                  <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Reserve Price</p>
                  <p className="text-lg font-bold text-gray-900 flex items-center">
                    <IndianRupee className="w-4 h-4 mr-0.5" /> {(selectedProperty.reserve_price / 100000).toFixed(1)} Lakhs
                  </p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Est. Market Value</p>
                  <p className="text-lg font-semibold text-gray-400 line-through flex items-center">
                    <IndianRupee className="w-4 h-4 mr-0.5" /> {(selectedProperty.market_value / 100000).toFixed(1)} Lakhs
                  </p>
                </div>
              </div>
              
              {/* Deal Assessment */}
              <div className="space-y-2">
                <div className="flex justify-between items-center text-sm border-b border-gray-100 pb-2">
                  <span className="text-gray-500">Discount Offered:</span>
                  <span className="font-bold text-emerald-600">-{selectedProperty.discount}% Below Market</span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-gray-500">Auction Date:</span>
                  <span className="font-semibold text-gray-800">{selectedProperty.auction_date}</span>
                </div>
              </div>
              
              {/* Associated Project */}
              {selectedProperty.project_id && (
                <div className="p-4 bg-indigo-50 border border-indigo-100 rounded-xl">
                  <h4 className="text-xs font-bold text-indigo-900 uppercase tracking-wider mb-1">Nearby Infrastructure Benefit</h4>
                  <p className="text-xs text-indigo-700 leading-relaxed mb-3">
                    This property is located in close proximity to a major verified infrastructure project, boosting its future capital appreciation.
                  </p>
                  <Link 
                    href={`/projects/${selectedProperty.project_id}`}
                    className="inline-flex items-center gap-1.5 text-xs font-bold text-indigo-600 hover:text-indigo-800 transition-colors"
                  >
                    <span>View Infrastructure Project Details</span>
                    <span className="text-sm">→</span>
                  </Link>
                </div>
              )}
            </div>
            
            {/* Modal Footer */}
            <div className="p-4 bg-gray-50 border-t border-gray-150 flex justify-end gap-3">
              <button 
                onClick={() => setSelectedProperty(null)}
                className="px-4 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-100 transition-colors"
              >
                Close
              </button>
              <a 
                href={selectedProperty.backing_authority?.includes("LDA") ? "https://www.ldalucknow.in" : "https://ibapi.in"}
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-2 bg-gray-900 text-white rounded-lg text-sm font-semibold hover:bg-gray-800 transition-colors flex items-center gap-1"
              >
                <span>Participate in Auction</span>
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
