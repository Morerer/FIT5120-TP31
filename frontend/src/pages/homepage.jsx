import React from 'react';
import { Link } from 'react-router-dom';

export default function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-4xl font-bold mb-2">In the City:</h1>
      <p className="text-lg text-gray-500 mb-6">Melbourne Parking For You</p>
      <div className="flex gap-4">
        <Link to="/map">
          <button className="px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
            Map
          </button>
        </Link>
        <Link to="/trends">
          <button className="px-6 py-2 bg-green-500 text-white rounded hover:bg-green-600">
            Trends
          </button>
        </Link>
        <Link to="/eco-insights">
          <button className="px-6 py-2 bg-emerald-500 text-white rounded hover:bg-emerald-600">
            Eco
          </button>
        </Link>
        <Link to="/data">
          <button className="px-6 py-2 bg-gray-800 text-white rounded hover:bg-gray-900">
            See Datas
          </button>
        </Link>
      </div>
    </div>
  );
}
