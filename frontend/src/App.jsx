import React from 'react';
import { Routes, Route } from 'react-router-dom';

import Navbar from './components/navbar.jsx';
import HomePage from './pages/HomePage.jsx';
import MapPage from './pages/MapPage.jsx';
import TrendsPage from './pages/TrendsPage.jsx';

// 占位：后续有独立页面时再替换为 import
const EcoInsightsPage = () => <div className="p-8 text-xl">Eco-Insights (coming soon)</div>;
const NotFound = () => <div className="p-8 text-xl">404 Not Found</div>;

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/map" element={<MapPage />} />
        <Route path="/trends" element={<TrendsPage />} />
        <Route path="/eco-insights" element={<EcoInsightsPage />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </div>
  );
}
