"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getProjects } from "@/lib/api";
import StatusIndicator from "@/components/projects/StatusIndicator";
import { MapPin, Calendar, IndianRupee, HardHat } from "lucide-react";

import { useCity } from "@/components/providers/CityProvider";

export default function ProjectsDirectoryPage() {
  const [projects, setProjects] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [projectType, setProjectType] = useState("");
  const [status, setStatus] = useState("");
  const { city, cityName } = useCity();

  // Reset filters when city changes
  useEffect(() => {
    setProjectType("");
    setStatus("");
  }, [city]);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const params: any = { city };
        if (projectType) params.project_type = projectType;
        if (status) params.status = status;
        const data = await getProjects(params);
        setProjects(data.items || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [city, projectType, status]);

  return (
    <div className="max-w-6xl mx-auto p-4 md:p-8">
      <div className="mb-8 flex flex-col md:flex-row md:items-end md:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Projects Directory</h1>
          <p className="text-gray-600">Browse all verified infrastructure projects across {cityName}.</p>
        </div>
        
        {/* Filters */}
        <div className="flex flex-wrap items-center gap-3">
          <select 
            className="bg-white border border-gray-200 text-gray-900 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none shadow-sm min-w-[160px]"
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
            className="bg-white border border-gray-200 text-gray-900 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none shadow-sm min-w-[160px]"
            value={status}
            onChange={(e) => setStatus(e.target.value)}
          >
            <option value="">All Statuses</option>
            <option value="announced">Proposed</option>
            <option value="approved">Approved</option>
            <option value="under_construction">Under Construction</option>
            <option value="completed">Completed</option>
            <option value="on_hold">On Hold</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-12 text-gray-500">Loading projects...</div>
      ) : projects.length === 0 ? (
        <div className="text-center py-12 text-gray-500 bg-white border border-gray-200 rounded-xl">
          No projects found matching the selected filters.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <Link key={project.id} href={`/projects/${project.id}`} className="group block h-full">
              <div className="bg-white border border-gray-200 rounded-xl p-5 hover:shadow-md transition-shadow h-full flex flex-col">
                <div className="flex justify-between items-start mb-3">
                  <StatusIndicator status={project.status} />
                  {project.is_verified && (
                    <span className="w-2 h-2 rounded-full bg-emerald-500 mt-1.5" title="Verified Data"></span>
                  )}
                </div>
                
                <h3 className="font-bold text-gray-900 text-lg mb-2 group-hover:text-indigo-600 transition-colors line-clamp-2">
                  {project.name}
                </h3>
                
                <div className="space-y-2 mt-auto pt-4 border-t border-gray-100">
                  <div className="flex items-center text-sm text-gray-600 gap-2">
                    <HardHat className="w-4 h-4 text-gray-400" />
                    <span className="capitalize">{project.project_type.replace('_', ' ')}</span>
                  </div>
                  <div className="flex items-center text-sm text-gray-600 gap-2">
                    <MapPin className="w-4 h-4 text-gray-400" />
                    <span>{project.city}</span>
                  </div>
                  {project.budget_crore && (
                    <div className="flex items-center text-sm text-gray-600 gap-2">
                      <IndianRupee className="w-4 h-4 text-gray-400" />
                      <span>₹{project.budget_crore} Cr</span>
                    </div>
                  )}
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

