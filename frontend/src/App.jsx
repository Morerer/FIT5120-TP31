import React from 'react';
import { Routes, Route } from 'react-router-dom';

import Navbar from './components/navbar.jsx';
import HomePage from './pages/HomePage.jsx';
import MapPage from './pages/MapPage.jsx';
import TrendsPage from './pages/TrendsPage.jsx';
import EcoInsightsPage from './pages/EcoInsightsPage.jsx'; 

const NotFound = () => <div className="p-8 text-xl">404 Not Found</div>;

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/map" element={<MapPage />} />
        <Route path="/trends" element={<TrendsPage />} />
        <Route path="/eco-insights" element={<EcoInsightsPage />} /> {/* New Page */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </div>
  );
}
