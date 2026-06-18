import React from 'react';

interface StatusIndicatorProps {
  status: string;
}

export default function StatusIndicator({ status }: StatusIndicatorProps) {
  let colorClass = "bg-gray-100 text-gray-800";
  let label = status.replace('_', ' ');

  switch (status.toLowerCase()) {
    case 'announced':
      colorClass = "bg-blue-100 text-blue-800";
      break;
    case 'approved':
      colorClass = "bg-indigo-100 text-indigo-800";
      break;
    case 'under_construction':
      colorClass = "bg-amber-100 text-amber-800";
      break;
    case 'completed':
      colorClass = "bg-emerald-100 text-emerald-800";
      break;
    case 'on_hold':
      colorClass = "bg-orange-100 text-orange-800";
      break;
    case 'cancelled':
      colorClass = "bg-red-100 text-red-800";
      break;
  }

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize ${colorClass}`}>
      {label}
    </span>
  );
}
