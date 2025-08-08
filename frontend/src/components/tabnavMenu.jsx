import { TabNav } from '@radix-ui/themes'
import { useState } from 'react'

export default function TabNavMenu() {
  const [activeTab, setActiveTab] = useState('account')

  const tabs = [
    { key: 'account', label: 'Account' },
    { key: 'documents', label: 'Documents' },
    { key: 'settings', label: 'Settings' },
  ]

  return (
    <div className="w-full flex flex-col items-center">
      <TabNav.Root size="2" color="indigo">
        {tabs.map((tab) => (
          <TabNav.Link
            key={tab.key}
            active={activeTab === tab.key}
            onClick={() => setActiveTab(tab.key)}
            href="#"
          >
            {tab.label}
          </TabNav.Link>
        ))}
      </TabNav.Root>

      <div className="mt-6">
        {activeTab === 'account' && <p>Account info here</p>}
        {activeTab === 'documents' && <p>List of documents here</p>}
        {activeTab === 'settings' && <p>Settings form here</p>}
      </div>
    </div>
  )
}
