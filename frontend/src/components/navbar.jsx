'use client'
import * as NavigationMenu from '@radix-ui/react-navigation-menu'
import { ChevronDownIcon } from '@radix-ui/react-icons'

export default function Navbar() {
  return (
    <NavigationMenu.Root className="relative flex justify-between items-center bg-gray-800 text-white px-6 py-4">
      <div className="text-xl font-bold">Melbourne Parking</div>

      <NavigationMenu.List className="flex gap-6">
        <NavigationMenu.Item>
          <NavigationMenu.Link className="hover:text-blue-400" href="#">Home</NavigationMenu.Link>
        </NavigationMenu.Item>
        <NavigationMenu.Item>
          <NavigationMenu.Link className="hover:text-blue-400" href="#">Trends</NavigationMenu.Link>
        </NavigationMenu.Item>
        <NavigationMenu.Item>
          <NavigationMenu.Link className="hover:text-blue-400" href="#">Insights</NavigationMenu.Link>
        </NavigationMenu.Item>
        <NavigationMenu.Item>
          <NavigationMenu.Link className="hover:text-blue-400" href="#">Eco-Insights</NavigationMenu.Link>
        </NavigationMenu.Item>
      </NavigationMenu.List>
    </NavigationMenu.Root>
  )
}
