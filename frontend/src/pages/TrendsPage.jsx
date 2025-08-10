import { useState, useMemo, useEffect } from 'react';
import {
  LineChart, Line, AreaChart, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

const TABS = [
  { key: 'car', label: 'Car Ownership' },
  { key: 'congestion', label: 'Congestion' },
  { key: 'population', label: 'Population' },
  { key: 'both', label: 'Population vs Congestion' },
];


const BASE = import.meta.env.VITE_API_BASE_URL || '';

export default function TrendsPage() {
  const [active, setActive] = useState('population');
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);

  const title = useMemo(() => {
    switch (active) {
      case 'car': return 'Car Ownership (per 100 Households)';
      case 'congestion': return 'Congestion Index';
      case 'population': return 'Melbourne CBD Population (×10k)';
      case 'both': return 'Population vs Congestion';
      default: return '';
    }
  }, [active]);

  const yearRange = useMemo(() => {
    const ys = rows
      .map(r => parseInt(r.year, 10))
      .filter(n => Number.isFinite(n))
      .sort((a, b) => a - b);
    if (!ys.length) return null;
    return `${ys[0]}–${ys[ys.length - 1]}`;
  }, [rows]);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      setLoading(true);
      setErr(null);
      try {
        let path = '/api/trends/population';
        if (active === 'congestion') path = '/api/trends/congestion';
        else if (active === 'car') path = '/api/trends/car-ownership';
        else if (active === 'both') path = '/api/trends/combined';

        const res = await fetch(`${BASE}${path}`);
        if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
        const json = await res.json();

        // Normalise to the shape recharts expects for each tab
        // Backend returns: { data: [{ year: "YYYY", population?, congestion?, car? }], ... }
        const normalised = (json?.data || []).map(d => ({
          year: String(d.year),
          population: d.population ?? undefined,
          congestion: d.congestion ?? undefined,
          car: d.car ?? undefined,
        }));

        if (!cancelled) setRows(normalised);
      } catch (e) {
        if (!cancelled) setErr(e.message || 'Failed to load data');
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    load();
    return () => { cancelled = true; };
  }, [active]);

  return (
    <div className="px-4 md:px-8 py-8 bg-gray-100 min-h-[calc(100vh-64px)]">
      <h2 className="text-center text-sm tracking-[0.3em] text-gray-500">HISTORICAL TRENDS</h2>
      <h1 className="text-center text-3xl md:text-5xl font-bold mt-2">MELBOURNE CBD</h1>

      <div className="mt-8 grid grid-cols-1 md:grid-cols-[300px,1fr] gap-6">
        <aside className="bg-white/80 backdrop-blur rounded-2xl shadow-sm p-4 md:p-6 border border-gray-100">
          <h3 className="text-sm font-semibold text-gray-600 mb-3">TREND GRAPHS</h3>
          <div className="flex md:block gap-3 md:gap-0">
            {TABS.map(tab => (
              <button
                key={tab.key}
                onClick={() => setActive(tab.key)}
                className={`w-full md:mb-3 px-4 py-2 rounded-lg border text-sm transition
                  ${active === tab.key ? 'bg-gray-900 text-white border-gray-900 shadow'
                                       : 'bg-white hover:bg-gray-50 border-gray-300 text-gray-700'}`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </aside>

        <section className="bg-white rounded-2xl shadow-sm border border-gray-100 p-2 md:p-4">
          <div className="rounded-xl bg-gradient-to-br from-gray-50 to-white p-4 md:p-6">
            <div className="flex items-baseline justify-between mb-2">
              <h4 className="text-lg md:text-xl font-semibold">{title}</h4>
              <span className="text-xs text-gray-500">{yearRange || '—'}</span>
            </div>

            <div className="h-[380px] md:h-[460px]">
              {loading ? (
                <div className="h-full flex items-center justify-center text-sm text-gray-500">
                  Loading…
                </div>
              ) : err ? (
                <div className="h-full flex items-center justify-center text-sm text-red-600">
                  Error: {err}
                </div>
              ) : (
                <ResponsiveContainer width="100%" height="100%">
                  {active === 'population' ? (
                    <AreaChart data={rows}>
                      <defs>
                        <linearGradient id="gPop" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#60a5fa" stopOpacity={0.4}/>
                          <stop offset="95%" stopColor="#60a5fa" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                      <XAxis dataKey="year" />
                      <YAxis />
                      <Tooltip />
                      <Area type="monotone" dataKey="population" stroke="#3b82f6" fill="url(#gPop)" strokeWidth={2} />
                    </AreaChart>
                  ) : active === 'congestion' ? (
                    <LineChart data={rows}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                      <XAxis dataKey="year" />
                      <YAxis />
                      <Tooltip />
                      <Line type="monotone" dataKey="congestion" stroke="#f59e0b" strokeWidth={2} dot={false}/>
                    </LineChart>
                  ) : active === 'car' ? (
                    <LineChart data={rows}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                      <XAxis dataKey="year" />
                      <YAxis />
                      <Tooltip />
                      <Line type="monotone" dataKey="car" stroke="#10b981" strokeWidth={2} />
                    </LineChart>
                  ) : (
                    <LineChart data={rows}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                      <XAxis dataKey="year" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Line type="monotone" dataKey="population" name="Population (×10k)" stroke="#3b82f6" strokeWidth={2} dot={false}/>
                      <Line type="monotone" dataKey="congestion" name="Congestion" stroke="#ef4444" strokeWidth={2} dot={false}/>
                    </LineChart>
                  )}
                </ResponsiveContainer>
              )}
            </div>

            <p className="text-xs text-gray-500 mt-3">
              Data fetched from backend endpoints:
              {` `}
              {active === 'population' && '/api/trends/population'}
              {active === 'congestion' && '/api/trends/congestion'}
              {active === 'car' && '/api/trends/car-ownership'}
              {active === 'both' && '/api/trends/combined'}
            </p>
          </div>
        </section>
      </div>
    </div>
  );
}
