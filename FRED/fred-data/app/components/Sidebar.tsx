'use client';

import { useState } from 'react';

interface MenuItemProps {
  icon: React.ReactNode;
  label: string;
  isActive?: boolean;
  onClick?: () => void;
}

function MenuItem({ icon, label, isActive, onClick }: MenuItemProps) {
  return (
    <button
      onClick={onClick}
      className={`w-full flex items-center justify-between px-4 py-3 text-left transition-colors ${
        isActive
          ? 'bg-blue-600 text-white'
          : 'text-gray-700 hover:bg-gray-100'
      }`}
    >
      <div className="flex items-center gap-3">
        <span className="text-lg">{icon}</span>
        <span className="font-medium">{label}</span>
      </div>
      <svg
        width="16"
        height="16"
        viewBox="0 0 16 16"
        fill="none"
        className={isActive ? 'text-white' : 'text-gray-400'}
      >
        <path
          d="M6 4l4 4-4 4"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </button>
  );
}

export default function Sidebar() {
  const [activeItem, setActiveItem] = useState('Key Indicators');

  const menuItems = [
    { icon: '📈', label: 'Key Indicators' },
    { icon: '📈', label: 'Inflation' },
    { icon: '💼', label: 'Employment' },
    { icon: '📊', label: 'Interest Rates' },
    { icon: '📈', label: 'Economic Growth' },
    { icon: '🌐', label: 'Exchange Rates' },
    { icon: '🏠', label: 'Housing' },
    { icon: '🛒', label: 'Consumer Spending' },
  ];

  return (
    <div className="w-72 h-screen bg-white border-r border-gray-200 flex flex-col">
      {/* Header */}
      <div className="p-6 border-b border-gray-200">
        <h1 className="text-xl font-bold text-gray-900">FRED Indicators</h1>
        <p className="text-sm text-gray-600 mt-1">Economic Data Dashboard</p>
      </div>

      {/* Menu Items */}
      <nav className="flex-1 py-4">
        {menuItems.map((item) => (
          <MenuItem
            key={item.label}
            icon={item.icon}
            label={item.label}
            isActive={activeItem === item.label}
            onClick={() => setActiveItem(item.label)}
          />
        ))}
      </nav>

      {/* Footer */}
      <div className="p-6 border-t border-gray-200">
        <p className="text-xs text-gray-500">
          Data provided by Federal Reserve Economic Data (FRED)
        </p>
      </div>
    </div>
  );
}
