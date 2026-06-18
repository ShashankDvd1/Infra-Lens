import React from 'react';

export default function SavedOpportunitiesPage() {
  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Saved Opportunities</h1>
      <p className="text-gray-600 mb-8">View and manage the infrastructure projects you're tracking.</p>
      
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 text-center text-gray-500">
        You haven't saved any opportunities yet. Explore the map to find interesting projects!
      </div>
    </div>
  );
}
