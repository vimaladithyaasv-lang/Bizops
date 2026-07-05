import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Building2, Users, Search, Star } from 'lucide-react';
import axios from 'axios';

export default function CategoryPage() {
  const { categoryId, areaId, businesscount, population } = useParams();
  const [searchQuery, setSearchQuery] = useState('');
  
  const BASE_URL = 'http://127.0.0.1:5000';
  // const BASE_URL = 'https://bizops-hackathon.onrender.com'

  interface BusinessInfo {
    Address__point: string;
    Name__point: string;
    Rating__point: number;
  }

  interface AreaBusinessData {
    businesses_information: BusinessInfo[];
    prediction_messages: string[];
    predictions: string[];
  }

  const [businessCategories, setBusinessCategories] = useState<AreaBusinessData>({
    businesses_information: [],
    prediction_messages: [],
    predictions: []
  });

  const filteredCompetitors = businessCategories.businesses_information.filter(business => {
    const businessName = business?.Name__point || '';
    const businessAddress = business?.Address__point || '';
    const searchTerm = searchQuery.toLowerCase();
    
    return businessName.toLowerCase().includes(searchTerm) ||
           businessAddress.toLowerCase().includes(searchTerm);
  });

  useEffect(() => {
    const fetchBusinessCategories = async () => {
      try {
        const response = await axios.post(`${BASE_URL}/api/predict-opportunity`, [{
          area_name: areaId,
          business_category: categoryId?.replace('_','/'),
          Count_of_businesses: businesscount,
          Population_of_area: population
        }]);
        
        const data = typeof response.data === "string" ? JSON.parse(response.data) : response.data;
        console.log(data);
        setBusinessCategories(data);
      } catch (error) {
        console.error('Error fetching business categories:', error);
        setBusinessCategories({
          businesses_information: [],
          prediction_messages: ['Error loading data'],
          predictions: ['N/A']
        });
      }
    };

    fetchBusinessCategories();
  }, [areaId, categoryId, businesscount, population]);

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <div className="flex items-center space-x-3">
            <Building2 className="h-6 w-6 text-indigo-500" />
            <div>
              <h3 className="text-lg font-medium text-gray-900">Total Business</h3>
              <p className="text-2xl font-bold">{businesscount}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm">
          <div className="flex items-center space-x-3">
            <Users className="h-6 w-6 text-indigo-500" />
            <div>
              <h3 className="text-lg font-medium text-gray-900">Total Population</h3>
              <p className="text-2xl font-bold">{population}</p>
            </div>
          </div>
        </div>

        <div className="bg-green-50 p-6 rounded-lg shadow-sm">
          <h3 className="text-lg font-medium text-green-900">Opportunity Analyzer</h3>
          <p className="text-2xl font-bold text-green-700">
            {businessCategories.predictions?.[0]?.toUpperCase() || 'N/A'}
          </p>
          <p className="mt-1 text-sm text-green-600">
            {businessCategories.prediction_messages?.[0] || 'No prediction available'}
          </p>
        </div>
      </div>

      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-bold text-gray-900">Competitors</h2>
          <div className="relative w-64">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search businesses..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            <Search className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {filteredCompetitors.map((business, index) => (
            <div key={index} className="bg-white p-4 rounded-lg shadow-sm">
              <div className="h-12 w-12 bg-indigo-100 rounded-lg mb-4 flex items-center justify-center">
                <Building2 className="h-6 w-6 text-indigo-500" />
              </div>
              <h3 className="font-medium text-gray-900">{business.Name__point || 'Unknown Business'}</h3>
              <p className="text-sm text-gray-600 mt-1">{business.Address__point || 'No address available'}</p>
              <div className="flex items-center mt-2">
                <Star className="h-4 w-4 text-yellow-400" />
                <span className="ml-1 text-sm text-gray-600">
                  {business.Rating__point === 0 ? "No Ratings" : business.Rating__point}
                </span>
              </div>
            </div>
          ))}
          {filteredCompetitors.length === 0 && (
            <div className="col-span-full text-center py-8 text-gray-500">
              No businesses found matching your search criteria
            </div>
          )}
        </div>
      </div>
    </div>
  );
}