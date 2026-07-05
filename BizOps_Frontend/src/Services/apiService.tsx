import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:5000/api';
// const BASE_URL = 'https://bizops-hackathon.onrender.com/api'


export const fetchBusinessCategories = async () => {
  const response = await axios.get(`${BASE_URL}/business-categories`);
  return response.data;
};

export const fetchAreaNames = async () => {
  const response = await axios.get(`${BASE_URL}/area-names`);
  return response.data;
};

export const fetchSummedPopulation = async () => {
  const response = await axios.get(`${BASE_URL}/summed-population`);
  return response.data;
};
