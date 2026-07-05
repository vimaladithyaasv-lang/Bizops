import { Link } from 'react-router-dom';
import { Building2, User } from 'lucide-react';

export default function Navbar() {
  return (
    <nav className="bg-white shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center space-x-2">
            <Building2 className="h-8 w-8 text-indigo-500" />
            <span className="text-xl font-bold text-gray-900">Bizops</span>
          </Link>
          <div className="flex items-center space-x-8">
            <Link to="/" className="text-gray-700 hover:text-gray-900">Home</Link>
            {/* <Link to="/business-categories">Business Categories</Link>
            <Link to="/area-names">Area Names</Link>
            <Link to="/summed-population">Summed Population</Link> */}
            <button className="p-2 rounded-full bg-indigo-100">
              <User className="h-5 w-5 text-indigo-500" />
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}