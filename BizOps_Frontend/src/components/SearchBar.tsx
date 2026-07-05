import React, { useState } from 'react';
import { Search } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface SearchBarProps {
  AREAS: string[];
}

export default function Autocomplete({ AREAS }: SearchBarProps) {
  const [query, setQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();

  const filteredAreas =
    query.trim() &&
    AREAS.filter(area =>
      area.toLowerCase().includes(query.toLowerCase())
    );

  const handleSelect = (area: string) => {
    setQuery(area); // Update the input value to the selected area
    setIsOpen(false); // Close the suggestions dropdown
    navigate(`/area/${area.toUpperCase()}`); // Navigate to the selected area
  };

  return (
    <div className="relative max-w-xl mx-auto">
      <div className="relative">
        <input
          type="text"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setIsOpen(true);
          }}
          onFocus={() => setIsOpen(true)}
          placeholder="Search areas..."
          className="w-full px-4 py-3 pl-12 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
        />
        <Search className="absolute left-4 top-3.5 h-5 w-5 text-gray-400" />
      </div>

      {isOpen && filteredAreas && filteredAreas.length > 0 && (
        <ul className="absolute w-full mt-2 bg-white rounded-lg shadow-lg border border-gray-200 z-10 max-h-48 overflow-y-auto">
          {filteredAreas.map(area => (
            <li
              key={area}
              onClick={() => handleSelect(area)}
              className="px-4 py-3 text-left hover:bg-gray-50 transition-colors cursor-pointer"
            >
              {area}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
