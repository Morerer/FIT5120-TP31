'use client';
import * as NavigationMenu from '@radix-ui/react-navigation-menu';
import { NavLink } from 'react-router-dom';

export default function Navbar() {
  const linkClass = ({ isActive }) =>
    `hover:text-blue-400 ${isActive ? 'text-blue-300' : ''}`;

  return (
    <NavigationMenu.Root className="relative flex justify-between items-center bg-gray-800 text-white px-6 py-4">
      <div className="text-xl font-bold">Melbourne Parking</div>

      <NavigationMenu.List className="flex gap-6 items-center">
        <NavigationMenu.Item>
          <NavLink to="/" className={linkClass}>Home</NavLink>
        </NavigationMenu.Item>
        <NavigationMenu.Item>
          <NavLink to="/trends" className={linkClass}>Map</NavLink>
        </NavigationMenu.Item>
        <NavigationMenu.Item>
          <NavLink to="/insights" className={linkClass}>Trends</NavLink>
        </NavigationMenu.Item>
        <NavigationMenu.Item>
          <NavLink to="/eco-insights" className={linkClass}>Eco-Insights</NavLink>
        </NavigationMenu.Item>
      </NavigationMenu.List>
    </NavigationMenu.Root>
  );
}
