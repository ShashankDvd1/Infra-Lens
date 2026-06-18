import React from 'react';

export default function AIInvestmentAssistantPage() {
  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">AI Investment Assistant</h1>
      <p className="text-gray-600 mb-8">Get personalized investment recommendations based on your budget and goals.</p>
      
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 max-w-2xl">
        <h2 className="text-xl font-bold mb-6">Tell us what you're looking for</h2>
        
        <form className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Investment Budget (₹)</label>
            <input type="text" placeholder="e.g. 50 Lakhs" className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Preferred Asset Type</label>
            <select className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
              <option>Residential Land</option>
              <option>Commercial Space</option>
              <option>Agricultural Land</option>
              <option>Distress Properties</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Time Horizon</label>
            <select className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
              <option>Short Term (1-3 years)</option>
              <option>Medium Term (3-7 years)</option>
              <option>Long Term (7+ years)</option>
            </select>
          </div>
          
          <button type="button" className="w-full bg-blue-600 text-white font-semibold py-3 rounded-lg hover:bg-blue-700 transition">
            Generate AI Recommendations
          </button>
        </form>
      </div>
    </div>
  );
}
