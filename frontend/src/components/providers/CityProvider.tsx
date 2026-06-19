"use client";

import React, { createContext, useContext, useState, useEffect } from "react";

type City = "lucknow" | "pune" | "hyderabad";

interface CityContextType {
  city: City;
  setCity: (city: City) => void;
  cityName: string;
  cityCenter: [number, number];
}

const CityContext = createContext<CityContextType | undefined>(undefined);

const CITY_DETAILS: Record<City, { name: string; center: [number, number] }> = {
  lucknow: { name: "Lucknow", center: [26.8467, 80.9462] },
  pune: { name: "Pune", center: [18.5204, 73.8567] },
  hyderabad: { name: "Hyderabad", center: [17.3850, 78.4867] },
};

export function CityProvider({ children }: { children: React.ReactNode }) {
  const [city, setCityState] = useState<City>("lucknow");

  // Read initial city from localStorage if available
  useEffect(() => {
    const saved = localStorage.getItem("city_focus") as City;
    if (saved && ["lucknow", "pune", "hyderabad"].includes(saved)) {
      setCityState(saved);
    }
  }, []);

  const setCity = (newCity: City) => {
    setCityState(newCity);
    localStorage.setItem("city_focus", newCity);
  };

  const details = CITY_DETAILS[city];

  return (
    <CityContext.Provider
      value={{
        city,
        setCity,
        cityName: details.name,
        cityCenter: details.center,
      }}
    >
      {children}
    </CityContext.Provider>
  );
}

export function useCity() {
  const context = useContext(CityContext);
  if (context === undefined) {
    throw new Error("useCity must be used within a CityProvider");
  }
  return context;
}
