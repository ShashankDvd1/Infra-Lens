"use client";

import { useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// Fix for default Leaflet icon paths in Next.js
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
  iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});

interface MapComponentProps {
  geojsonData: any;
}

// Custom icon creator using the emoji and color
const createCustomIcon = (emoji: string, color: string) => {
  return L.divIcon({
    className: "custom-div-icon",
    html: `<div style="background-color: ${color}; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3); font-size: 16px;">
             ${emoji}
           </div>`,
    iconSize: [30, 30],
    iconAnchor: [15, 15],
    popupAnchor: [0, -15],
  });
};

export default function MapComponent({ geojsonData }: MapComponentProps) {
  const defaultCenter: [number, number] = [26.8467, 80.9462]; // Lucknow

  return (
    <MapContainer 
      center={defaultCenter} 
      zoom={11} 
      style={{ height: "100%", width: "100%", zIndex: 1 }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      
      {geojsonData?.features?.map((feature: any) => {
        const coords = feature.geometry.coordinates;
        const props = feature.properties;
        const latLng: [number, number] = [coords[1], coords[0]];
        
        return (
          <Marker 
            key={props.id} 
            position={latLng}
            icon={createCustomIcon(props.icon, props.color)}
          >
            <Popup>
              <div className="p-1">
                <h3 className="font-bold text-sm mb-1">{props.name}</h3>
                <div className="text-xs text-gray-600 mb-2">
                  <span className="capitalize">{props.project_type.replace('_', ' ')}</span>
                  <span className="mx-1">•</span>
                  <span className="capitalize">{props.status.replace('_', ' ')}</span>
                </div>
                {props.budget_crore && (
                  <div className="text-xs mb-1">
                    <strong>Budget:</strong> ₹{props.budget_crore} Cr
                  </div>
                )}
                {props.expected_completion && (
                  <div className="text-xs mb-2">
                    <strong>Expected:</strong> {new Date(props.expected_completion).toLocaleDateString()}
                  </div>
                )}
                <a 
                  href={`/projects/${props.id}`}
                  className="inline-block mt-2 px-3 py-1 bg-blue-600 text-white text-xs font-medium rounded hover:bg-blue-700"
                >
                  View Details
                </a>
              </div>
            </Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
}
