import { useState, useMemo } from 'react';
import {
  BarChart, Bar,
  LineChart, Line,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer
} from 'recharts';

/** —— Mock data (can be replaced with API later) —— */
// Unit emissions from different modes of transport（g CO2 / km /）
const emissionPerKm = [
  { mode: 'Walking',     co2: 0   },
  { mode: 'Cycling',     co2: 0   },
  { mode: 'Tram',        co2: 40  },
  { mode: 'Train',       co2: 25  },
  { mode: 'Bus',         co2: 75  },
  { mode: 'Car (Solo)',  co2: 180 },
  { mode: 'Car (Shared)',co2: 95  },
];

// 2014–2024 Percentage of travel by mode — sample data
const modalShare = [
  { year: '2014', walk: 8,  bike: 3,  tram: 18, train: 22, bus: 14, car: 35 },
  { year: '2016', walk: 9,  bike: 4,  tram: 19, train: 22, bus: 13, car: 33 },
  { year: '2018', walk: 10, bike: 5,  tram: 19, train: 23, bus: 12, car: 31 },
  { year: '2020', walk: 11, bike: 6,  tram: 18, train: 22, bus: 12, car: 31 },
  { year: '2022', walk: 10, bike: 7,  tram: 18, train: 23, bus: 12, car: 30 },
  { year: '2024', walk: 11, bike: 8,  tram: 18, train: 24, bus: 12, car: 27 },
];

const TABS = [
  { key: 'co2',  label: 'Estimated CO2 Emissions' },
  { key: 'mode', label: 'Transport Mode Comparisons' },
];

export default function EcoInsightsPage() {
  const [active, setActive] = useState('co2');

  const title = useMemo(() => (
    active === 'co2'
      ? 'Estimated CO₂ Emissions by Transport Mode (g / km / person)'
      : 'Transport Mode Share in the CBD (%)'
  ), [active]);

  return (
    <div className="px-4 md:px-8 py-8 bg-gray-100 min-h-[calc(100vh-64px)]">
      <h2 className="text-center text-sm tracking-[0.3em] text-gray-500">
        TRANSPORT INSIGHTS IN THE CBD
      </h2>
      <h1 className="text-center text-3xl md:text-5xl font-bold mt-2">
        ENVIRONMENTAL IMPACT
      </h1>

      <div className="mt-8 grid grid-cols-1 md:grid-cols-[300px,1fr] gap-6">
        {/* Left side: Button panel */}
        <aside className="bg-white/80 backdrop-blur rounded-2xl shadow-sm p-4 md:p-6 border border-gray-100">
          <h3 className="text-sm font-semibold text-gray-600 mb-3">ECO-INSIGHT GRAPHS</h3>
          <div className="flex md:block gap-3 md:gap-0">
            {TABS.map(tab => (
              <button
                key={tab.key}
                onClick={() => setActive(tab.key)}
                className={[
                  "w-full md:mb-3 px-4 py-2 rounded-lg border text-sm transition",
                  active === tab.key
                    ? "bg-gray-900 text-white border-gray-900 shadow"
                    : "bg-white hover:bg-gray-50 border-gray-300 text-gray-700"
                ].join(' ')}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </aside>

        {/* Right side: Chart area */}
        <section className="bg-white rounded-2xl shadow-sm border border-gray-100 p-2 md:p-4">
          <div className="rounded-xl bg-gradient-to-br from-gray-50 to-white p-4 md:p-6">
            <div className="flex items-baseline justify-between mb-2">
              <h4 className="text-lg md:text-xl font-semibold">{title}</h4>
              <span className="text-xs text-gray-500">
                {active === 'co2' ? 'Per-km emissions' : '2014–2024'}
              </span>
            </div>

            <div className="h-[380px] md:h-[460px]">
              <ResponsiveContainer width="100%" height="100%">
                {active === 'co2' ? (
                  <BarChart data={emissionPerKm} barSize={28}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis dataKey="mode" tick={{ fontSize: 12 }} interval={0} />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar
                      dataKey="co2"
                      name="CO₂ (g/km/person)"
                      radius={[8, 8, 0, 0]}
                      fill="#22c55e"
                    />
                  </BarChart>
                ) : (
                  <LineChart data={modalShare}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis dataKey="year" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="walk" name="Walking" stroke="#0ea5e9" strokeWidth={2} dot={false}/>
                    <Line type="monotone" dataKey="bike" name="Cycling" stroke="#10b981" strokeWidth={2} dot={false}/>
                    <Line type="monotone" dataKey="tram" name="Tram" stroke="#6366f1" strokeWidth={2} dot={false}/>
                    <Line type="monotone" dataKey="train" name="Train" stroke="#3b82f6" strokeWidth={2} dot={false}/>
                    <Line type="monotone" dataKey="bus"  name="Bus"  stroke="#f59e0b" strokeWidth={2} dot={false}/>
                    <Line type="monotone" dataKey="car"  name="Car"  stroke="#ef4444" strokeWidth={2} dot={false}/>
                  </LineChart>
                )}
              </ResponsiveContainer>
            </div>

            <p className="text-xs text-gray-500 mt-3">
              * Mock data for demo. Replace with real datasets (e.g., emissions by mode, yearly modal split).
            </p>
          </div>
        </section>
      </div>
    </div>
  );
}
