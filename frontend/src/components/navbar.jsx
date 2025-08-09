'use client';
import * as NavigationMenu from '@radix-ui/react-navigation-menu';
import { NavLink } from 'react-router-dom';

export default function Navbar() {
  const linkClass = ({ isActive }) =>
    `px-1 transition-colors duration-200 hover:text-blue-400 ${
      isActive ? 'text-blue-300 font-semibold' : ''
    }`;

  return (
    <NavigationMenu.Root className="relative flex justify-between items-center bg-gray-800 text-white px-6 py-4">
      {/* Logo / Title */}
      <div className="text-xl font-bold">Melbourne Parking</div>

      {/* Navigation Links */}
      <NavigationMenu.List className="flex gap-6 items-center">
        <NavigationMenu.Item>
          <NavLink to="/" end className={linkClass}>
            Home
          </NavLink>
        </NavigationMenu.Item>
        <NavigationMenu.Item>
          <NavLink to="/map" className={linkClass}>
            Map
          </NavLink>
        </NavigationMenu.Item>
        <NavigationMenu.Item>
          <NavLink to="/trends" className={linkClass}>
            Trends
          </NavLink>
        </NavigationMenu.Item>
        <NavigationMenu.Item>
          <NavLink to="/eco-insights" className={linkClass}>
            Eco-Insights
          </NavLink>
        </NavigationMenu.Item>
      </NavigationMenu.List>
    </NavigationMenu.Root>
  );
}
