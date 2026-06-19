"use client";

import { useState, useEffect } from "react";
import { useSession } from "next-auth/react";
import { Bell, Trash2, Plus, X, AlertCircle } from "lucide-react";
import Link from "next/link";
import { getAlerts, createAlert, deleteAlert } from "@/lib/api";

export default function AlertsPage() {
  const { data: session, status } = useSession();
  const [alerts, setAlerts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);

  // Form states
  const [areaSlug, setAreaSlug] = useState("");
  const [projectType, setProjectType] = useState("");
  const [minOpportunityScore, setMinOpportunityScore] = useState(50);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const projectTypes = [
    { label: "Metro Rail", value: "metro" },
    { label: "Expressway", value: "expressway" },
    { label: "Ring Road", value: "ring_road" },
    { label: "IT City / Tech Hub", value: "it_city" },
    { label: "Wellness / Medical City", value: "wellness_city" },
    { label: "Integrated Township", value: "township" },
    { label: "Logistics Park", value: "logistics_park" },
    { label: "Awas Vikas Housing", value: "awas_vikas" },
    { label: "Elevated Road / Flyover", value: "flyover" },
    { label: "Other Infrastructure", value: "other" },
  ];

  const areas = [
    // Lucknow
    { name: "Gomti Nagar (Lucknow)", slug: "gomti-nagar", city: "Lucknow" },
    { name: "Gomti Nagar Extension (Lucknow)", slug: "gomti-nagar-extension", city: "Lucknow" },
    { name: "Shaheed Path Corridor (Lucknow)", slug: "shaheed-path", city: "Lucknow" },
    { name: "Kanpur Road Corridor (Lucknow)", slug: "kanpur-road", city: "Lucknow" },
    { name: "Amar Shaheed Path (Lucknow)", slug: "amar-shaheed-path", city: "Lucknow" },
    // Pune
    { name: "Hinjawadi (Pune)", slug: "hinjawadi", city: "Pune" },
    { name: "Baner (Pune)", slug: "baner", city: "Pune" },
    // Hyderabad
    { name: "Gachibowli (Hyderabad)", slug: "gachibowli", city: "Hyderabad" },
    { name: "Madhapur (Hyderabad)", slug: "madhapur", city: "Hyderabad" },
  ];

  useEffect(() => {
    if (status === "authenticated" && session?.accessToken) {
      loadAlerts();
    } else if (status === "unauthenticated") {
      setLoading(false);
    }
  }, [status, session]);

  const loadAlerts = async () => {
    setLoading(true);
    try {
      const data = await getAlerts(session!.accessToken as string);
      setAlerts(data || []);
    } catch (err) {
      console.error("Failed to load alerts:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateAlert = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!session?.accessToken) return;
    setSubmitting(true);
    setError("");

    try {
      await createAlert(
        {
          area_slug: areaSlug || undefined,
          project_type: projectType || undefined,
          min_opportunity_score: minOpportunityScore,
        },
        session.accessToken as string
      );
      setAreaSlug("");
      setProjectType("");
      setMinOpportunityScore(50);
      setShowAddForm(false);
      await loadAlerts();
    } catch (err: any) {
      console.error(err);
      setError("Failed to create alert. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeleteAlert = async (id: string) => {
    if (!session?.accessToken) return;
    if (!confirm("Are you sure you want to delete this alert?")) return;

    try {
      await deleteAlert(id, session.accessToken as string);
      setAlerts(alerts.filter((alert) => alert.id !== id));
    } catch (err) {
      console.error("Failed to delete alert:", err);
      alert("Failed to delete alert.");
    }
  };

  if (status === "loading" || loading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="text-gray-500 text-lg">Loading your alerts...</div>
      </div>
    );
  }

  if (status === "unauthenticated") {
    return (
      <div className="max-w-md mx-auto mt-20 p-6 bg-white border border-gray-200 rounded-2xl shadow-sm text-center">
        <Bell className="w-12 h-12 text-emerald-600 mx-auto mb-4" />
        <h2 className="text-xl font-bold text-gray-900 mb-2">Sign In Required</h2>
        <p className="text-gray-600 mb-6">You must be logged in to create and manage custom infrastructure alerts.</p>
        <Link
          href="/login"
          className="inline-block w-full py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl transition-colors"
        >
          Sign In
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-4 md:p-8">
      <div className="flex justify-between items-center border-b border-gray-200 pb-6 mb-8">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-emerald-100 rounded-lg text-emerald-600">
            <Bell className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Custom Alerts</h1>
            <p className="text-gray-600 text-sm mt-1">Get notified of high-growth projects in your target areas.</p>
          </div>
        </div>
        <button
          onClick={() => setShowAddForm(!showAddForm)}
          className="flex items-center gap-2 bg-emerald-600 text-white px-4 py-2.5 rounded-xl text-sm font-semibold hover:bg-emerald-700 transition-colors"
        >
          {showAddForm ? <X className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
          {showAddForm ? "Cancel" : "New Alert"}
        </button>
      </div>

      {showAddForm && (
        <form
          onSubmit={handleCreateAlert}
          className="bg-white border border-gray-200 rounded-2xl p-6 mb-8 shadow-sm max-w-2xl"
        >
          <h2 className="text-lg font-bold text-gray-900 mb-4">Set Alert Criteria</h2>
          {error && (
            <div className="bg-red-50 border border-red-100 text-red-700 p-3 rounded-lg text-sm mb-4 flex items-center gap-2">
              <AlertCircle className="w-4 h-4" /> {error}
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Target Area (Optional)</label>
              <select
                value={areaSlug}
                onChange={(e) => setAreaSlug(e.target.value)}
                className="w-full bg-gray-50 border border-gray-200 text-gray-900 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              >
                <option value="">Any Area</option>
                {areas.map((a) => (
                  <option key={a.slug} value={a.slug}>
                    {a.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Project Type (Optional)</label>
              <select
                value={projectType}
                onChange={(e) => setProjectType(e.target.value)}
                className="w-full bg-gray-50 border border-gray-200 text-gray-900 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              >
                <option value="">Any Project Type</option>
                {projectTypes.map((t) => (
                  <option key={t.value} value={t.value}>
                    {t.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-1">Minimum Opportunity Score</label>
            <input
              type="range"
              min="0"
              max="100"
              value={minOpportunityScore}
              onChange={(e) => setMinOpportunityScore(Number(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-emerald-600"
            />
            <div className="mt-2 text-center text-lg font-bold text-emerald-600">
              Score: {minOpportunityScore}+
            </div>
          </div>

          <button
            type="submit"
            disabled={submitting}
            className="w-full py-3 bg-emerald-600 text-white rounded-xl font-bold hover:bg-emerald-700 transition-colors disabled:opacity-75"
          >
            {submitting ? "Creating..." : "Save Alert Subscription"}
          </button>
        </form>
      )}

      {alerts.length === 0 ? (
        <div className="text-center py-16 bg-white border border-gray-200 rounded-2xl shadow-sm">
          <Bell className="w-12 h-12 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-1">No Active Alerts</h3>
          <p className="text-gray-500 text-sm max-w-sm mx-auto mb-6">
            Set up an alert to receive email notifications when new infrastructure projects are detected.
          </p>
          <button
            onClick={() => setShowAddForm(true)}
            className="px-4 py-2 bg-emerald-50 text-emerald-700 text-sm font-semibold rounded-lg hover:bg-emerald-100 transition-colors"
          >
            Create Your First Alert
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {alerts.map((alert) => {
            const areaObj = areas.find((a) => a.slug === alert.area_slug);
            const typeObj = projectTypes.find((t) => t.value === alert.project_type);

            return (
              <div
                key={alert.id}
                className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow relative flex flex-col justify-between"
              >
                <div>
                  <div className="flex justify-between items-start mb-4">
                    <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                      Active
                    </span>
                    <button
                      onClick={() => handleDeleteAlert(alert.id)}
                      className="text-gray-400 hover:text-red-600 transition-colors p-1.5 hover:bg-red-50 rounded-lg"
                      title="Delete Alert"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>

                  <h3 className="font-bold text-gray-900 text-lg mb-4">Notification Criteria</h3>

                  <div className="space-y-3 border-t border-gray-100 pt-4 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-500">Target Area:</span>
                      <span className="font-semibold text-gray-800 text-right">
                        {areaObj ? areaObj.name : "Any Location"}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Project Type:</span>
                      <span className="font-semibold text-gray-800 text-right">
                        {typeObj ? typeObj.label : "Any Type"}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Min Opportunity Score:</span>
                      <span className="font-semibold text-emerald-600 text-right">
                        {alert.min_opportunity_score ?? 0}+
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
