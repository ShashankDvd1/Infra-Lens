"use client";

import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const dummyData = [
  { name: 'Jan', queries: 4000, alerts: 2400, saved: 2400 },
  { name: 'Feb', queries: 3000, alerts: 1398, saved: 2210 },
  { name: 'Mar', queries: 2000, alerts: 9800, saved: 2290 },
  { name: 'Apr', queries: 2780, alerts: 3908, saved: 2000 },
  { name: 'May', queries: 1890, alerts: 4800, saved: 2181 },
  { name: 'Jun', queries: 2390, alerts: 3800, saved: 2500 },
  { name: 'Jul', queries: 3490, alerts: 4300, saved: 2100 },
];

export default function AnalyticsDashboard() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Platform Analytics</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
          <h3 className="text-gray-500 text-sm font-medium">Total AI Queries</h3>
          <p className="text-3xl font-bold mt-2">19,550</p>
          <span className="text-green-500 text-sm font-medium">↑ 12% this month</span>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
          <h3 className="text-gray-500 text-sm font-medium">Active Subscriptions</h3>
          <p className="text-3xl font-bold mt-2">3,490</p>
          <span className="text-green-500 text-sm font-medium">↑ 4% this month</span>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
          <h3 className="text-gray-500 text-sm font-medium">Scraped Projects</h3>
          <p className="text-3xl font-bold mt-2">842</p>
          <span className="text-green-500 text-sm font-medium">↑ 22% this month</span>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 h-96">
        <h2 className="text-lg font-semibold mb-4">User Activity Trends</h2>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={dummyData}
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="queries" fill="#8884d8" name="AI Queries" />
            <Bar dataKey="saved" fill="#82ca9d" name="Saved Opportunities" />
            <Bar dataKey="alerts" fill="#ffc658" name="Alerts Sent" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
