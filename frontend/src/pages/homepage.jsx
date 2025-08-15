import React from "react";
import { Link } from "react-router-dom";
import { MapPin, LineChart, Leaf } from "lucide-react"; // Icons

export default function HomePage() {
  return (
    <main className="min-h-[calc(100vh-64px)] bg-slate-100 flex items-center justify-center px-6 py-16">
      <div className="w-full max-w-6xl">
        {/* Title + description */}
        <div className="text-center mb-10">
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-slate-900">
            In the City:
          </h1>
          <p className="mt-3 text-lg text-slate-600 max-w-2xl mx-auto">
            Melbourne Parking For You, explore live traffic, usage trends, and eco
            insights to plan smarter CBD trips.
          </p>
        </div>

        {/* Card grid (centered) */}
        <section className="grid grid-cols-1 sm:grid-cols-2 gap-6 max-w-4xl mx-auto place-items-center">
          <CardLink
            to="/trends"
            title="Trends"
            desc="yearly and monthly patterns."
            accent="from-emerald-50 to-emerald-100"
            icon={<LineChart className="h-8 w-8 text-emerald-600" />}
          />
          <CardLink
            to="/eco-insights"
            title="Eco"
            desc="Congestion & emissions indicators."
            accent="from-lime-50 to-lime-100"
            icon={<Leaf className="h-8 w-8 text-lime-600" />}
          />
        </section>
      </div>
    </main>
  );
}

/** Tailwind-only Card Link */
function CardLink({ to, title, desc, accent, icon }) {
  return (
    <Link to={to} className="group block w-full max-w-sm">
      <div className="h-full rounded-2xl border border-slate-200 bg-white shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
        <div className="p-5">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
            <span className="text-xs font-medium text-slate-600 bg-slate-100 px-2 py-1 rounded-md group-hover:bg-slate-200"></span>
          </div>
          <p className="mt-1 text-sm text-slate-600">{desc}</p>
          <div className={`mt-4 h-28 rounded-md bg-gradient-to-br ${accent} flex items-center justify-center`}>
            {icon}
          </div>
        </div>
      </div>
    </Link>
  );
}
