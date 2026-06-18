"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Map, List, MessageSquare, Compass, Bookmark, AlertTriangle, TrendingUp, FolderKanban } from "lucide-react";

export default function Sidebar() {
  const pathname = usePathname();

  const navItems = [
    { name: "Infrastructure Map", href: "/map", icon: Map },
    { name: "Projects Directory", href: "/projects", icon: FolderKanban },
    { name: "Area Intelligence", href: "/area", icon: Compass },
    { name: "Saved Opportunities", href: "/saved", icon: Bookmark },
    { name: "Distress Properties", href: "/distress", icon: AlertTriangle },
    { name: "AI Investment Assistant", href: "/invest", icon: TrendingUp },
    { name: "Ask AI", href: "/ask-ai", icon: MessageSquare },
  ];

  return (
    <div className="w-64 bg-white border-r border-gray-200 h-screen flex flex-col fixed left-0 top-0 z-20">
      <div className="h-16 flex items-center px-6 border-b border-gray-200">
        <Link href="/" className="flex items-center gap-2">
          <div className="w-8 h-8 bg-emerald-600 rounded-lg flex items-center justify-center text-white font-bold text-xl">L</div>
          <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-emerald-600 to-teal-600">LandScope</span>
        </Link>
      </div>

      <div className="px-6 py-4 border-b border-gray-100">
        <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">City Focus</label>
        <select className="w-full bg-gray-50 border border-gray-200 text-gray-900 rounded-lg p-2 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none">
          <option value="lucknow">Lucknow, UP</option>
          <option value="pune">Pune, MH</option>
          <option value="hyderabad">Hyderabad, TS</option>
        </select>
      </div>

      <nav className="flex-1 px-4 py-6 space-y-1">
        <p className="px-2 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-4">Platform</p>
        {navItems.map((item) => {
          const isActive = pathname === item.href || pathname.startsWith(`${item.href}/`);
          const Icon = item.icon;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                isActive 
                  ? "bg-indigo-50 text-indigo-700" 
                  : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
              }`}
            >
              <Icon className={`w-5 h-5 ${isActive ? "text-indigo-600" : "text-gray-400"}`} />
              {item.name}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-gray-800">
        <div className="bg-gray-800 rounded-lg p-4 text-center">
          <p className="text-xs text-gray-400 mb-2">Lucknow MVP</p>
          <div className="w-full bg-gray-700 rounded-full h-1.5 mb-1">
            <div className="bg-emerald-500 h-1.5 rounded-full" style={{ width: '45%' }}></div>
          </div>
          <p className="text-[10px] text-gray-500 uppercase">20 Projects Tracked</p>
        </div>
      </div>
    </div>
  );
}
