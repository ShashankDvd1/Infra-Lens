"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getProjects } from "@/lib/api";
import StatusIndicator from "@/components/projects/StatusIndicator";
import { MapPin, Calendar, IndianRupee, HardHat } from "lucide-react";

export default function ProjectsDirectoryPage() {
  const [projects, setProjects] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await getProjects();
        setProjects(data.items || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <div className="max-w-6xl mx-auto p-4 md:p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Projects Directory</h1>
        <p className="text-gray-600">Browse all verified infrastructure projects across the region.</p>
      </div>

      {loading ? (
        <div className="text-center py-12">Loading projects...</div>
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
