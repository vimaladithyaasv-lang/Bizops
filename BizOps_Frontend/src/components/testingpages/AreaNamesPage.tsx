import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface AreaName {
  StandardizedAreaName: string;
}

const AreaNamesPage: React.FC = () => {
  //const BASE_URL = 'http://127.0.0.1:5000/api';
  const BASE_URL = 'https://bizops-hackathon.onrender.com/api';
  const [areaNames, setAreaNames] = useState<AreaName[]>([]);

  useEffect(() => {
    const fetchAreaNames = async () => {
      const response = await axios.get(`${BASE_URL}/area-names`);
      setAreaNames(response.data);
    };

    fetchAreaNames();
  }, []);

  return (
    <div>
      <h1>Area Names</h1>
      <ul>
        {areaNames.map((area, index) => (
          <li key={index}>{area["StandardizedAreaName"]}</li>
        ))}
      </ul>
    </div>
  );
};

export default AreaNamesPage;
