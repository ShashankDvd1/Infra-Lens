import React from 'react';
import { ExternalLink, FileText, Globe, Newspaper } from 'lucide-react';

interface SourceBadgeProps {
  sourceType: string;
  title: string;
  url?: string;
  authorityName?: string;
}

export default function SourceBadge({ sourceType, title, url, authorityName }: SourceBadgeProps) {
  let Icon = FileText;
  let colorClass = "bg-gray-50 text-gray-700 border-gray-200";

  switch (sourceType) {
    case 'government_notification':
    case 'tender_document':
      Icon = FileText;
      colorClass = "bg-blue-50 text-blue-700 border-blue-200";
      break;
    case 'authority_website':
    case 'master_plan':
      Icon = Globe;
      colorClass = "bg-emerald-50 text-emerald-700 border-emerald-200";
      break;
    case 'news_article':
      Icon = Newspaper;
      colorClass = "bg-amber-50 text-amber-700 border-amber-200";
      break;
  }

  const content = (
    <div className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md border text-xs font-medium ${colorClass} hover:shadow-sm transition-shadow`}>
      <Icon className="w-3.5 h-3.5" />
      <span className="truncate max-w-[200px]">{authorityName || title}</span>
      {url && <ExternalLink className="w-3 h-3 ml-1 opacity-70" />}
    </div>
  );

  if (url) {
    return (
      <a href={url} target="_blank" rel="noopener noreferrer" className="inline-block" title={title}>
        {content}
      </a>
    );
  }

  return <div className="inline-block" title={title}>{content}</div>;
}
