import React from 'react';

export default function AlertsPage() {
  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">My Alerts</h1>
      <p className="text-gray-600 mb-8">Manage your notifications for new projects and status updates.</p>
      
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold">Active Subscriptions</h2>
          <button className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700">
            + New Alert
          </button>
        </div>
        <div className="text-center text-gray-500 py-8">
          No active alerts. Set up an alert to get notified when new projects match your criteria.
        </div>
      </div>
    </div>
  );
}
