import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface SummedPopulation {
  TotalPopulationSum: number;
  MalePopulationSum: number;
  FemalePopulationSum: number;
}

const SummedPopulationPage: React.FC = () => {
  const [summedPopulation, setSummedPopulation] = useState<SummedPopulation | null>(null);

  useEffect(() => {
    const fetchSummedPopulation = async () => {
      const response = await axios.get('/api/summed-population');
      setSummedPopulation(response.data);
    };

    fetchSummedPopulation();
  }, []);

  return (
    <div>
      <h1>Summed Population</h1>
      {summedPopulation && (
        <div>
          <p>Total Population: {summedPopulation.TotalPopulationSum}</p>
          <p>Male Population: {summedPopulation.MalePopulationSum}</p>
          <p>Female Population: {summedPopulation.FemalePopulationSum}</p>
        </div>
      )}
    </div>
  );
};

export default SummedPopulationPage;
