import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface BusinessCategory {
  BusinessCategory: string;
  Count: number;
}

const BusinessCategoriesPage: React.FC = () => {
  const [businessCategories, setBusinessCategories] = useState<BusinessCategory[]>([]);

  // const BASE_URL = 'http://127.0.0.1:5000/api';
  const BASE_URL = 'https://bizops-hackathon.onrender.com/api';
  useEffect(() => {
    const fetchBusinessCategories = async () => {
      const response = await axios.get(`${BASE_URL}/business-categories`);
      setBusinessCategories(response.data);
    };

    fetchBusinessCategories();
  }, []);

  return (
    <div>
      <h1>Business Categories</h1>
      <ul>
        {businessCategories.map((category, index) => (
          <li key={index}>
            {category.BusinessCategory}: {category.Count}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default BusinessCategoriesPage;
