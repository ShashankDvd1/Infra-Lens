"use client";

import { useState, useEffect } from "react";
import { useSession } from "next-auth/react";
import { Bookmark, MapPin } from "lucide-react";
import Link from "next/link";
import { fetchAPI } from "@/lib/api";
import StatusIndicator from "@/components/projects/StatusIndicator";

export default function SavedOpportunitiesPage() {
  const { data: session, status } = useSession();
  const [saved, setSaved] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (status === "authenticated" && session?.accessToken) {
      const fetchSaved = async () => {
        try {
          const res = await fetchAPI("/users/saved", {
            headers: { Authorization: `Bearer ${session.accessToken}` }
          });
          setSaved(res);
        } catch (error) {
          console.error("Failed to fetch saved opportunities", error);
        } finally {
          setLoading(false);
        }
      };
      fetchSaved();
    } else if (status === "unauthenticated") {
      setLoading(false);
    }
  }, [status, session]);

  if (status === "loading" || loading) return <div className="p-8 text-center text-gray-500">Loading...</div>;

  if (status === "unauthenticated") {
    return (
      <div className="p-8 text-center">
        <h2 className="text-xl text-gray-700 mb-4">Please log in to view your saved opportunities.</h2>
        <Link href="/login" className="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-700">Sign In</Link>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-4 md:p-8">
      <div className="flex items-center gap-3 mb-8">
        <div className="p-2 bg-emerald-100 rounded-lg text-emerald-600">
          <Bookmark className="w-6 h-6" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900">Saved Opportunities</h1>
      </div>

      {saved.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 rounded-xl border border-dashed border-gray-300">
          <Bookmark className="w-12 h-12 text-gray-400 mx-auto mb-3" />
          <p className="text-gray-500">You haven't saved any projects yet.</p>
          <Link href="/projects" className="mt-4 inline-block text-emerald-600 hover:underline">
            Browse Projects
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {saved.map((item) => (
            <div key={item.id} className="bg-white border border-gray-200 rounded-xl p-5 hover:shadow-lg transition-shadow">
              <div className="flex justify-between items-start mb-3">
                <StatusIndicator status={item.project?.status} />
                <button className="text-emerald-600 hover:text-emerald-700">
                  <Bookmark className="w-5 h-5 fill-current" />
                </button>
              </div>
              <Link href={`/projects/${item.project?.id}`}>
                <h3 className="text-lg font-bold text-gray-900 hover:text-emerald-700 mb-2 line-clamp-2">
                  {item.project?.project_name}
                </h3>
              </Link>
              <div className="flex items-center gap-1.5 text-sm text-gray-500 mb-4">
                <MapPin className="w-4 h-4" /> {item.project?.city}
              </div>
              {item.notes && (
                <div className="bg-yellow-50 p-3 rounded-lg text-sm text-yellow-800 border border-yellow-100 mb-4">
                  <strong>Notes:</strong> {item.notes}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
