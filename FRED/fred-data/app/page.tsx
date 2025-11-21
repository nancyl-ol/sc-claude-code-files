'use client';

import { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import Sidebar from './components/Sidebar';
import {
  fetchCPIData,
  fetchUnemploymentData,
  fetch10YearTreasuryData,
  fetch3MonthTreasuryData,
} from './services/fredApi';

interface ChartCardProps {
  title: string;
  data: Array<{ date: string; value: number }>;
  yAxisLabel: string;
  domain?: [number, number];
  ticks?: number[];
}

function ChartCard({ title, data, yAxisLabel, domain, ticks }: ChartCardProps) {
  return (
    <div className="bg-[#D9D9D9] rounded-sm p-4 h-[480px] w-full">
      <h2 className="text-2xl font-bold mb-4">{title}</h2>
      <div className="bg-[#E8EEF2] p-4 h-[394px]">
        <div className="flex items-start mb-2">
          <div className="flex items-center gap-2">
            <span className="text-sm font-semibold">FRED</span>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" className="text-blue-600">
              <path d="M3 3h18v18H3z" fill="currentColor" opacity="0.1"/>
              <path d="M6 6l12 12M6 18l12-12" stroke="currentColor" strokeWidth="2"/>
            </svg>
            <div className="w-8 h-0.5 bg-blue-600"></div>
            <span className="text-sm text-gray-600">{title}</span>
          </div>
        </div>
        <ResponsiveContainer width="100%" height="85%">
          <LineChart data={data} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="0" stroke="#ccc" vertical={false} />
            <XAxis
              dataKey="date"
              tick={{ fontSize: 12 }}
              tickLine={false}
              axisLine={{ stroke: '#000' }}
            />
            <YAxis
              label={{ value: yAxisLabel, angle: -90, position: 'insideLeft', style: { fontSize: 12 } }}
              tick={{ fontSize: 12 }}
              tickLine={false}
              axisLine={{ stroke: '#000' }}
              domain={domain || ['auto', 'auto']}
              ticks={ticks}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #ccc',
                borderRadius: '4px',
                fontSize: '12px'
              }}
              formatter={(value: number) => value.toFixed(5)}
            />
            <Line
              type="monotone"
              dataKey="value"
              stroke="#2563eb"
              strokeWidth={2.5}
              dot={false}
              isAnimationActive={false}
            />
          </LineChart>
        </ResponsiveContainer>
        <div className="flex justify-between items-center mt-2 text-xs text-gray-600">
          <div>
            <p>Source: Organization for Economic Co-operation and Development via FRED®</p>
            <p className="text-blue-600 italic">Shaded areas indicate U.S. recessions.</p>
          </div>
          <div className="flex items-center gap-2">
            <span>fred.stlouisfed.org</span>
            <button className="border border-blue-600 text-blue-600 px-2 py-1 rounded text-xs">
              Fullscreen ⛶
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function Home() {
  const [cpiData, setCpiData] = useState<Array<{ date: string; value: number }>>([]);
  const [laborData, setLaborData] = useState<Array<{ date: string; value: number }>>([]);
  const [interest10YData, setInterest10YData] = useState<Array<{ date: string; value: number }>>([]);
  const [interest3MData, setInterest3MData] = useState<Array<{ date: string; value: number }>>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const [cpi, unemployment, treasury10Y, treasury3M] = await Promise.all([
          fetchCPIData(),
          fetchUnemploymentData(),
          fetch10YearTreasuryData(),
          fetch3MonthTreasuryData(),
        ]);

        setCpiData(cpi);
        setLaborData(unemployment);
        setInterest10YData(treasury10Y);
        setInterest3MData(treasury3M);
      } catch (error) {
        console.error('Error loading FRED data:', error);
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  return (
    <div className="flex min-h-screen bg-[#F3F4F6]">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <main className="flex-1 p-8">
        {/* Dashboard Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Economic Indicators Dashboard
          </h1>
          <p className="text-lg text-gray-600">
            Real-time economic data from the Federal Reserve Economic Data (FRED) system
          </p>
        </div>

        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="text-xl text-gray-600">Loading economic data...</div>
          </div>
        ) : (
          /* Charts */
          <div className="max-w-[2100px] space-y-8">
            {/* First row: CPI and Labor Statistics */}
            <div className="grid grid-cols-2 gap-8">
              <ChartCard
                title="CPI - Growth Rate (Last 5 Years)"
                data={cpiData}
                yAxisLabel="Growth rate previous period"
              />
              <ChartCard
                title="Unemployment Rate (Last 5 Years)"
                data={laborData}
                yAxisLabel="Percent"
              />
            </div>

            {/* Second row: Interest Rates */}
            <div className="grid grid-cols-2 gap-8">
              <ChartCard
                title="10-Year Treasury Constant Maturity Rate"
                data={interest10YData}
                yAxisLabel="Percent"
              />
              <ChartCard
                title="3-Month Treasury Bill Rate"
                data={interest3MData}
                yAxisLabel="Percent"
              />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
