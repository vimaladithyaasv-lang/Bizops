import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import AreaPage from './pages/AreaPage';
import CategoryPage from './pages/CategoryPage';
import BusinessCategoriesPage from './components/testingpages/BusinessCategoriesPage';
import AreaNamesPage from './components/testingpages/AreaNamesPage';
import SummedPopulationPage from './components/testingpages/SummedPopulationPage';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/area/:areaId" element={<AreaPage />} />
            <Route path="/category/:areaId/:categoryId/:businesscount/:population" element={<CategoryPage />} />
            <Route path="/business-categories" element={<BusinessCategoriesPage />} />
            <Route path="/area-names" element={<AreaNamesPage />} />
            <Route path="/summed-population" element={<SummedPopulationPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
