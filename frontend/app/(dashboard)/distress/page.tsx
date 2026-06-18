import React from 'react';

export default function DistressPropertiesPage() {
  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Distress Properties & Auctions</h1>
      <p className="text-gray-600 mb-8">Discover high-value opportunities from bank auctions and distress sales.</p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-red-200 p-6">
          <div className="inline-block bg-red-100 text-red-700 text-xs font-bold px-2 py-1 rounded mb-4">Bank Auction</div>
          <h3 className="text-lg font-bold">Commercial Plot, Gomti Nagar</h3>
          <p className="text-sm text-gray-500 mt-2">12,000 SqFt • Base Price: ₹4.2 Cr</p>
          <div className="mt-4 pt-4 border-t border-gray-100">
            <p className="text-sm text-gray-600">Estimated Market Value: <span className="font-semibold text-green-600">₹6.5 Cr</span></p>
          </div>
        </div>
      </div>
    </div>
  );
}
