"use client";

import { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import { getMapMarkers } from "@/lib/api";

// Dynamically import Leaflet components to avoid SSR issues
const Map = dynamic(
  () => import("@/components/map/MapComponent"),
  { 
    ssr: false,
    loading: () => <div className="w-full h-full flex items-center justify-center bg-gray-100">Loading Map...</div>
  }
);

export default function MapPage() {
  const [markers, setMarkers] = useState<any>(null);
  const [projectType, setProjectType] = useState("");
  const [status, setStatus] = useState("");

  useEffect(() => {
    async function loadMarkers() {
      setMarkers(null);
      try {
        const params: any = {};
        if (projectType) params.project_type = projectType;
        if (status) params.status = status;
        const data = await getMapMarkers(params);
        setMarkers(data);
      } catch (error) {
        console.error("Failed to load map markers:", error);
      }
    }
    loadMarkers();
  }, [projectType, status]);

  return (
    <div className="flex h-screen w-full flex-col md:flex-row">
      <div className="w-full md:w-1/4 h-1/3 md:h-full bg-white p-4 overflow-y-auto border-r border-gray-200">
        <h1 className="text-2xl font-bold mb-4">Infrastructure Map</h1>
        <p className="text-gray-600 mb-4">Explore major infrastructure projects across Lucknow.</p>
        
        {/* Filters */}
        <div className="mb-4">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Filters</h2>
          <div className="p-3 bg-gray-50 rounded-lg flex flex-col gap-3">
            <select 
              className="w-full bg-white border border-gray-200 text-gray-900 rounded-md p-2 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              value={projectType}
              onChange={(e) => setProjectType(e.target.value)}
            >
              <option value="">All Project Types</option>
              <option value="metro">Metro</option>
              <option value="expressway">Expressway</option>
              <option value="ring_road">Ring Road</option>
              <option value="it_city">IT City</option>
              <option value="township">Township</option>
              <option value="flyover">Flyover</option>
              <option value="other">Other</option>
            </select>

            <select 
              className="w-full bg-white border border-gray-200 text-gray-900 rounded-md p-2 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              value={status}
              onChange={(e) => setStatus(e.target.value)}
            >
              <option value="">All Statuses</option>
              <option value="proposed">Proposed</option>
              <option value="approved">Approved</option>
              <option value="under_construction">Under Construction</option>
              <option value="completed">Completed</option>
              <option value="on_hold">On Hold</option>
            </select>
          </div>
        </div>

        {/* Project List will go here */}
        <div>
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Visible Projects</h2>
          {markers?.features?.map((f: any) => (
            <div key={f.properties.id} className="mb-2 p-3 bg-white border border-gray-100 rounded-lg shadow-sm hover:shadow-md transition-shadow">
              <div className="flex items-start gap-2">
                <span className="text-xl">{f.properties.icon}</span>
                <div>
                  <h3 className="font-medium text-sm text-gray-900">{f.properties.name}</h3>
                  <p className="text-xs text-gray-500 capitalize">{f.properties.project_type.replace('_', ' ')} • {f.properties.status.replace('_', ' ')}</p>
                </div>
              </div>
            </div>
          ))}
          {!markers && <div className="text-sm text-gray-500">Loading projects...</div>}
        </div>
      </div>
      
      <div className="w-full md:w-3/4 h-2/3 md:h-full relative">
        <Map geojsonData={markers} />
      </div>
    </div>
  );
}
