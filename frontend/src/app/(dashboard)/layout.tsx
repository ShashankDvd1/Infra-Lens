import Sidebar from "@/components/common/Sidebar";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 ml-64">
        {/* Simple top header could go here if needed, but for now just the content */}
        <main className="w-full h-full">
          {children}
        </main>
      </div>
    </div>
  );
}
