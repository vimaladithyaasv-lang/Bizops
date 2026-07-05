import { useState, useEffect } from 'react';
import SearchBar from '../components/SearchBar';
import axios from 'axios';

interface BusinessCategory {
  BusinessCategory: string;
  Count: number;
}

interface SummedPopulation {
  FemalePopulationSum: number;
  MalePopulationSum: number;
  TotalPopulationSum: number;
}

interface CityWiseDetails {
  AreaNames: string[];
  BusinessCategories: BusinessCategory[];
  SummedPopulation: SummedPopulation;
}

const BASE_URL = 'http://127.0.0.1:5000';

const AREA_DATA = [
  { name: "Abhiramapuram", description: "A serene residential area with proximity to Chennai's central locations." },
  { name: "Adambakkam", description: "A well-connected suburban area with residential and commercial growth." },
  { name: "Adyar", description: "A posh locality known for its greenery and proximity to the coastline." },
  { name: "Chennai", description: "The capital of Tamil Nadu, a hub of culture, commerce, and heritage." },
  // ... rest of your AREA_DATA array
];

export default function HomePage() {
  const [cityDetails, setCityDetails] = useState<CityWiseDetails | null>(null);
  const [mapHTML, setMapHTML] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAll = async () => {
      try {
        setLoading(true);
        setError(null);

        // FIX 1: Pass city_name param — your API requires it
        const [cityRes, mapRes] = await Promise.all([
          axios.get(`${BASE_URL}/api/data-by-city`, {
            params: { city_name: 'CHENNAI' },
          }),
          axios.post(`${BASE_URL}/api/mapData`, { area_name: 'CHENNAI' }),
        ]);

        setCityDetails(cityRes.data);
        setMapHTML(mapRes.data.toString());
      } catch (err: any) {
        console.error('API error:', err);
        setError(err?.message || 'Failed to load data');
      } finally {
        setLoading(false);
      }
    };

    fetchAll();
  }, []);

  const area = AREA_DATA.find((a) =>
    a.name.toLowerCase() === 'chennai'
  );

  const formatNumber = (num?: number) =>
    num != null ? num.toLocaleString('en-IN') : '—';

  return (
    <div className="space-y-8 p-6">
      {/* Header */}
      <div className="flex justify-between items-start mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">{area?.name ?? 'Chennai'}</h1>
          <p className="mt-2 text-gray-600 max-w-2xl">{area?.description}</p>
        </div>
      </div>

      {/* Search bar — only render when area names are available */}
      {cityDetails?.AreaNames && cityDetails.AreaNames.length > 0 && (
        <SearchBar AREAS={cityDetails.AreaNames} />
      )}

      {/* Map */}
      {/* FIX 2: Consistent height on both containers */}
      <div style={{ width: '100%', height: '600px', borderRadius: '8px', overflow: 'hidden' }}>
        {mapHTML ? (
          <iframe
            srcDoc={mapHTML}
            style={{ width: '100%', height: '100%', border: 'none' }}
            title="Chennai Map"
          />
        ) : (
          <div className="flex items-center justify-center h-full bg-gray-100 text-gray-500">
            {loading ? 'Map is loading...' : 'Map unavailable'}
          </div>
        )}
      </div>

      {/* Error state */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          Error: {error}
        </div>
      )}

      {/* Stats Section */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        {/* Population */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Population Statistics</h2>
          {loading ? (
            <p className="text-gray-400">Loading population data...</p>
          ) : (
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-gray-50 p-4 rounded-lg">
                <h3 className="text-sm text-gray-600">Total Population</h3>
                <p className="text-xl font-bold text-gray-900">
                  {formatNumber(cityDetails?.SummedPopulation?.TotalPopulationSum)}
                </p>
              </div>
              <div className="bg-indigo-50 p-4 rounded-lg">
                <h3 className="text-sm text-gray-600">Male</h3>
                <p className="text-xl font-bold text-indigo-900">
                  {formatNumber(cityDetails?.SummedPopulation?.MalePopulationSum)}
                </p>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <h3 className="text-sm text-gray-600">Female</h3>
                <p className="text-xl font-bold text-purple-900">
                  {formatNumber(cityDetails?.SummedPopulation?.FemalePopulationSum)}
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Business Categories */}
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Business Categories</h2>
          {loading ? (
            <p className="text-gray-400">Loading business data...</p>
          ) : cityDetails?.BusinessCategories?.length ? (
            // FIX 3: Added key prop
            <div className="grid grid-cols-3 gap-4">
              {cityDetails.BusinessCategories.map((data, index) => (
                <div key={`${data.BusinessCategory}-${index}`} className="bg-green-50 p-4 rounded-lg">
                  <h3 className="text-sm text-gray-600">{data.BusinessCategory || 'Unknown'}</h3>
                  <p className="text-xl font-bold text-green-900">{data.Count}</p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-400">No business data available.</p>
          )}
        </div>
      </div>
    </div>
  );
}