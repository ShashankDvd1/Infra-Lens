import React from 'react';

export default function AreaIntelligencePage({ params }: { params: { slug: string } }) {
  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      <header className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 capitalize">{params.slug.replace('-', ' ')} Intelligence Report</h1>
        <p className="text-gray-600 mt-2">Comprehensive area analysis and growth indicators.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h3 className="text-sm font-semibold text-gray-500 uppercase">Avg Price / SqFt</h3>
          <p className="text-3xl font-bold text-gray-900 mt-2">₹5,400</p>
          <span className="text-green-500 text-sm font-medium">↑ 12% YoY</span>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h3 className="text-sm font-semibold text-gray-500 uppercase">Growth Rate</h3>
          <p className="text-3xl font-bold text-gray-900 mt-2">High</p>
          <span className="text-blue-500 text-sm font-medium">Top 15% in City</span>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h3 className="text-sm font-semibold text-gray-500 uppercase">Active Projects</h3>
          <p className="text-3xl font-bold text-gray-900 mt-2">24</p>
          <span className="text-gray-500 text-sm font-medium">6 completing this year</span>
        </div>
      </div>

      <div className="mt-12 bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Infrastructure Impact</h2>
        <div className="space-y-4">
          <div className="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg">
            <div className="bg-blue-100 text-blue-600 p-3 rounded-full">
              🚆
            </div>
            <div>
              <h4 className="font-semibold text-gray-900">Metro Connectivity</h4>
              <p className="text-gray-600">Proposed Phase 2 extension will add 2 new stations within a 3km radius.</p>
            </div>
          </div>
          
          <div className="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg">
            <div className="bg-orange-100 text-orange-600 p-3 rounded-full">
              🛣️
            </div>
            <div>
              <h4 className="font-semibold text-gray-900">Highway Access</h4>
              <p className="text-gray-600">Direct connection to the new Outer Ring Road, reducing commute times by 20 mins.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
