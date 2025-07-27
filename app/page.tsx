import { Button } from "@/components/ui/button";

async function getBreakouts() {
  const res = await fetch("http://localhost:8000/api/breakouts", { cache: "no-store" });
  return res.json();
}

export default async function Dashboard() {
  const breakouts = await getBreakouts();

  return (
    <div className="min-h-screen flex bg-gray-50">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r flex flex-col">
        <div className="h-16 flex items-center justify-center border-b">
          <span className="text-xl font-bold text-blue-700">Breakout Scanner</span>
        </div>
        <nav className="flex-1 px-4 py-6 space-y-2">
          <Button variant="ghost" className="w-full justify-start">Dashboard</Button>
          <Button variant="ghost" className="w-full justify-start">Watchlist</Button>
          <Button variant="ghost" className="w-full justify-start">Settings</Button>
        </nav>
        <div className="p-4 border-t">
          <Button variant="outline" className="w-full">Logout</Button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>
          <Button>Refresh</Button>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow p-6 flex flex-col items-center">
            <span className="text-2xl font-bold text-blue-700">{breakouts.length}</span>
            <span className="text-gray-500">Total Breakouts</span>
          </div>
          {/* Add more summary cards here if needed */}
        </div>

        {/* Breakout Results Table */}
        <div className="bg-white rounded-xl shadow overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Symbol</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Breakout Up</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Breakout Down</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">FRD</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">FGD</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Inside Day</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">2+ Up</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">2+ Down</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Close</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Week High</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Week Low</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Month High</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Month Low</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {breakouts.map((item: any, idx: number) => (
                <tr key={idx} className="hover:bg-gray-50 transition">
                  <td className="px-4 py-2 font-semibold text-blue-700">{item.Symbol}</td>
                  <td className="px-4 py-2">{item.Breakout_Up ? "✅" : ""}</td>
                  <td className="px-4 py-2">{item.Breakout_Down ? "✅" : ""}</td>
                  <td className="px-4 py-2">{item.FRD ? "✅" : ""}</td>
                  <td className="px-4 py-2">{item.FGD ? "✅" : ""}</td>
                  <td className="px-4 py-2">{item.Inside_Day ? "✅" : ""}</td>
                  <td className="px-4 py-2">{item.TwoPlus_Up ? "✅" : ""}</td>
                  <td className="px-4 py-2">{item.TwoPlus_Down ? "✅" : ""}</td>
                  <td className="px-4 py-2">{item.Close}</td>
                  <td className="px-4 py-2">{item.Week_High}</td>
                  <td className="px-4 py-2">{item.Week_Low}</td>
                  <td className="px-4 py-2">{item.Month_High}</td>
                  <td className="px-4 py-2">{item.Month_Low}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}