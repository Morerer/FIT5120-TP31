import React from 'react';
import Navbar from './components/navbar';
import HeroSection from './components/herosection';
import './index.css';
import HomePage from './pages/homepage';
import { TabNav } from '@radix-ui/themes';
import TabNavMenu from './components/tabnavMenu';
function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      <HeroSection/>
    </div>
  );
}

export default App;
