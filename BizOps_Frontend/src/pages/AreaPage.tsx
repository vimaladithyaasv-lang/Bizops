
import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import Map from '../components/Map';
import axios from 'axios';

// const AREA_DATA = {
//   name: "Triplicane, Chennai",
//   description:
//     "Lorem ipsum is a dummy or placeholder text commonly used in graphic design, publishing, and web development to fill empty spaces in a layout that do not yet have content.",
//   totalPopulation: "1000",
//   male: "500",
//   female: "500",
//   totalBusiness: "4000",
//   categories: {
//     schools: 25,
//     hotels: 34,
//     parks: 15,
//   },
// };

interface BusinessCategory {
  "Business Category": string;
  Count: number;
}
 

interface SummedPopulation {
  "Female Population Sum": number;
  "Male Population Sum": number;
  "Total Population Sum": number;
  
}

interface AreaBusinessData {
  business_categories_area : BusinessCategory[];
  missing_categories : string[];
  population_sums : SummedPopulation;
}

let AREA_DATA  = [
    {"name": "Abhiramapuram", "description": "A serene residential area with proximity to Chennai's central locations."},
    {"name": "Adambakkam", "description": "A well-connected suburban area with residential and commercial growth."},
    {"name": "Adyar", "description": "A posh locality known for its greenery and proximity to the coastline."},
    {"name": "Alandur", "description": "A metro-connected area known for its accessibility and residential complexes."},
    {"name": "Alwarpet", "description": "A luxury residential neighborhood with premium properties and amenities."},
    {"name": "Ambattur", "description": "An industrial area that has also evolved into a residential hub."},
    {"name": "Aminjikarai", "description": "A lively area with a blend of old and new residential developments."},
    {"name": "Anakaputhur", "description": "A fast-growing suburban locality with affordable housing."},
    {"name": "Anna Nagar", "description": "A planned residential neighborhood with parks and wide roads."},
    {"name": "Arumbakkam", "description": "A centrally located area with a mix of residential and commercial spaces."},
    {"name": "Ashok Nagar", "description": "A popular area with metro connectivity and excellent amenities."},
    {"name": "Avadi", "description": "A growing suburb known for its affordable housing and military establishments."},
    {"name": "Ayanambakkam", "description": "A calm and developing residential locality."},
    {"name": "Ayanavaram", "description": "An old neighborhood with a vibrant local community and amenities."},
    {"name": "Balavinayagar Nagar", "description": "A residential locality with peaceful surroundings and modern developments."},
    {"name": "Besant Nagar", "description": "A coastal locality famous for Elliot's Beach and a vibrant social life."},
    {"name": "Cathedral Road", "description": "A commercial and residential stretch with upscale establishments."},
    {"name": "Chennai", "description": "The capital of Tamil Nadu, a hub of culture, commerce, and heritage."},
    {"name": "Chetpet", "description": "A centrally located residential area known for Chetpet Lake."},
    {"name": "Chindatripet", "description": "An old locality with a bustling wholesale market scene."},
    {"name": "Chintadripet", "description": "A historic area known for its textile and wholesale markets."},
    {"name": "Choolaimedu", "description": "A densely populated area with residential and commercial establishments."},
    {"name": "Doctor Radha Krishnan Salai", "description": "A prominent road connecting Marina Beach to upscale localities."},
    {"name": "East Coast Road", "description": "A scenic highway with resorts, entertainment spots, and coastal views."},
    {"name": "Egmore", "description": "A historic locality known for government offices and museums."},
    {"name": "Ekkatuthangal", "description": "An industrial area transitioning into a mixed-use residential zone."},
    {"name": "Elliots Beach", "description": "A popular beach in Besant Nagar, attracting tourists and locals alike."},
    {"name": "Ennore", "description": "An industrial area with a port and growing residential developments."},
    {"name": "Foreshore Estate", "description": "A quiet coastal area known for its scenic views and residential spaces."},
    {"name": "Gandhi Nagar", "description": "An upscale residential locality in Adyar with cultural and recreational hubs."},
    {"name": "George Town", "description": "Chennai's historic business district known for its markets and heritage buildings."},
    {"name": "Gopalapuram", "description": "A premium residential area close to schools, colleges, and amenities."},
    {"name": "Guduvanchery", "description": "A rapidly developing suburb with residential and commercial growth."},
    {"name": "Guindy", "description": "An industrial and IT hub, home to Guindy National Park and metro stations."},
    {"name": "Haddows Road", "description": "A posh locality with residential spaces and proximity to major offices."},
    {"name": "Indira Nagar", "description": "A residential locality with good connectivity and amenities."},
    {"name": "Injambakkam", "description": "A scenic coastal area with resorts and premium housing."},
    {"name": "Iyyappanthangal", "description": "A suburban area known for its affordable housing and connectivity."},
    {"name": "Jafferkhanpet", "description": "A residential locality with a strong community presence."},
    {"name": "K K Nagar", "description": "A planned residential neighborhood with green spaces and schools."},
    {"name": "Kattupakkam", "description": "A developing suburb with growing residential projects."},
    {"name": "Keelkattalai", "description": "A growing residential area with affordable housing options."},
    {"name": "Kilpauk", "description": "A central area with premium housing and healthcare facilities."},
    {"name": "Kodambakkam", "description": "A vibrant area known as the hub of Tamil cinema industry."},
    {"name": "Kodungaiyur", "description": "An industrial locality with affordable residential options."},
    {"name": "Kolathur", "description": "A suburban area with excellent connectivity and growing housing projects."},
    {"name": "Konnur", "description": "A locality with a mix of industrial and residential zones."},
    {"name": "Korattur", "description": "A residential area with a peaceful environment and good connectivity."},
    {"name": "Korukkupet", "description": "An industrial locality with growing infrastructure development."},
    {"name": "Kotturpuram", "description": "An upscale residential area known for its greenery and cultural hubs."},
    {"name": "Koyambedu", "description": "Famous for its wholesale market and major bus terminal."},
    {"name": "Madhavaram", "description": "A suburban locality with industrial and residential growth."},
    {"name": "Madipakkam", "description": "A growing suburb with good connectivity and modern housing."},
    {"name": "Maduravoyal", "description": "Known for its residential areas and proximity to Chennai Bypass."},
    {"name": "Mambalam", "description": "A bustling locality famous for its retail and residential options."},
    {"name": "Manali", "description": "An industrial area with growing residential developments."},
    {"name": "Mandavelli", "description": "A cultural and residential area with proximity to key locations."},
    {"name": "Mangadu", "description": "A serene locality with religious significance and growing housing projects."},
    {"name": "Marina Beach", "description": "A famous beach and one of the key landmarks of Chennai."},
    {"name": "Medavakkam", "description": "A rapidly developing residential suburb."},
    {"name": "Mogappair", "description": "A well-planned residential area with good schools and hospitals."},
    {"name": "Mount Road", "description": "A historic commercial stretch connecting key parts of Chennai."},
    {"name": "Mudichur", "description": "A growing suburban area with affordable housing."},
    {"name": "Mugappair", "description": "Known for its residential developments and connectivity to IT hubs."},
    {"name": "Mylapore", "description": "A cultural hub known for its temples, heritage, and lively community."},
    {"name": "Nandanam", "description": "A centrally located area with premium residential and commercial spaces."},
    {"name": "Navalur", "description": "A suburb on OMR known for IT parks and residential complexes."},
    {"name": "Neelankarai", "description": "A coastal locality with upscale villas and serene beaches."},
    {"name": "Nerkundram", "description": "A developing area with residential growth."},
    {"name": "Nesapakkam", "description": "A calm residential area with good connectivity."},
    {"name": "Nolambur", "description": "A fast-growing suburb with modern residential projects."},
    {"name": "Nungambakkam", "description": "A posh area known for its cultural, educational, and lifestyle offerings."},
    {"name": "Old Mahabalipuram Road", "description": "An IT corridor with commercial and residential developments."},
    {"name": "OMR", "description": "A prominent IT hub with premium housing and commercial spaces."},
    {"name": "Padupakkam", "description": "A residential area with peaceful surroundings."},
    {"name": "Pallavaram", "description": "A suburb with proximity to the airport and good residential options."},
    {"name": "Pallikaranai", "description": "A growing residential suburb near the IT corridor."},
    {"name": "Park Town", "description": "An area near Chennai Central, known for its bustling markets."},
    {"name": "Pattabiram", "description": "A suburban area with a mix of residential and industrial zones."},
    {"name": "Pattalam", "description": "A residential area with historic significance."},
    {"name": "Perambur", "description": "A vibrant area with good schools and transportation facilities."},
    {"name": "Poonamallee", "description": "A growing suburb with excellent connectivity to key highways."},
    {"name": "Porur", "description": "A well-connected area with IT parks and residential projects."},
    {"name": "Puzhal", "description": "Known for its lake and affordable housing."},
    {"name": "Puzhuthivakkam", "description": "A residential area with good community facilities."},
    {"name": "Ramapuram", "description": "A centrally located residential area with good amenities."},
    {"name": "Royapettah", "description": "A commercial hub with good residential options and shopping spots."},
    {"name": "Royapuram", "description": "A coastal area known for its port and old railway station."},
    {"name": "Saidapet", "description": "A well-connected area with a mix of residential and commercial spaces."},
    {"name": "Selaiyur", "description": "A suburban area with affordable housing and good connectivity."},
    {"name": "Shenoy Nagar", "description": "A peaceful residential area with parks and schools."},
    {"name": "Sholinganallur", "description": "An IT hub with premium residential and commercial developments."},
    {"name": "Siruseri", "description": "Known for its IT parks and residential projects."},
    {"name": "Sowcarpet", "description": "A historic area known for its wholesale market and North Indian community."},
    {"name": "St. Thomas Mount", "description": "A historic area with religious significance and residential growth."},
    {"name": "Tambaram", "description": "A growing suburb known for its connectivity and residential areas."},
    {"name": "Taramani", "description": "An IT hub with residential and commercial developments."},
    {"name": "Teynampet", "description": "A central locality with high-end residential and commercial properties."},
    {"name": "Tharamani", "description": "An IT corridor with residential and commercial spaces."},
    {"name": "Thiruvanmiyur", "description": "A coastal area with a mix of IT parks and cultural hubs."},
    {"name": "Thoraipakkam", "description": "An IT hub with premium housing and modern amenities."},
    {"name": "Thousand Lights", "description": "A centrally located area with a mix of commercial and residential spaces."},
    {"name": "Tirusulam", "description": "An area near Chennai Airport with growing infrastructure."},
    {"name": "Triplicane", "description": "A historic locality with cultural and residential significance."},
    {"name": "Vadapalani", "description": "Known for its film studios and residential neighborhoods."},
    {"name": "Valasaravakkam", "description": "A residential locality with good schools and amenities."},
    {"name": "Vandalur", "description": "Known for its zoo and growing residential projects."},
    {"name": "Vepery", "description": "A historic area with schools, colleges, and residential options."},
    {"name": "Villivakkam", "description": "A bustling area with affordable housing and markets."},
    {"name": "Virugambakkam", "description": "A residential locality with good connectivity and schools."},
    {"name": "Washermanpet", "description": "A historic area known for its diverse community and markets."},
    {"name": "West Mambalam", "description": "A residential area with vibrant shopping streets."},
    {"name": "Zamin Pallavaram", "description": "A suburban area with growing residential and commercial spaces."}
  ]



// const BASE_URL = 'https://bizops-hackathon.onrender.com'
const BASE_URL = 'http://127.0.0.1:5000'

export default function AreaPage() {
  const { areaId } = useParams();

  const [searchValue, setSearchValue] = useState("");
  const [filteredArea, setFilteredArea] = useState(null);

  const area = AREA_DATA.find((area) =>
    area.name.toLowerCase().includes(areaId?.toString().toLowerCase() || "")
  );

  

  // console.log(areaId)

  const [businessCategories, setBusinessCategories] = useState<AreaBusinessData>({
    business_categories_area : [],
    missing_categories : [],
    population_sums : {
      "Female Population Sum": 0,
      "Male Population Sum": 0,
      "Total Population Sum": 0
    }
  });
  const [mapHTML, setMapHTML] = useState<string>("");
  useEffect(() => {
    const fetchBusinessCategories = async () => {
      const response = await axios.post(`${BASE_URL}/api/data-by-area`,{area_name : areaId });
      console.log("response",(response.data))
      setBusinessCategories(response.data);
    };
    const LoadMap = async () => {
      const response = await axios.post(`${BASE_URL}/api/mapData`,{area_name :areaId});
      // console.log(response.data)
      setMapHTML(response.data.toString());
    };

    fetchBusinessCategories();
    LoadMap();
  }, []);
  console.log("businessCategories",businessCategories);

  return (
    <div className="space-y-8">
      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="flex justify-between items-start mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{area?.name}</h1>
            <p className="mt-2 text-gray-600 max-w-2xl">{area?.description}</p>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="text-center">
            <h3 className="text-lg font-medium">Total Population</h3>
            <p className="text-2xl font-bold text-indigo-600">{businessCategories?.population_sums['Total Population Sum']}</p>
          </div>
          <div className="text-center">
            <h3 className="text-lg font-medium">Male</h3>
            <p className="text-2xl font-bold text-blue-600">{businessCategories?.population_sums['Male Population Sum']}</p>
          </div>
          <div className="text-center">
            <h3 className="text-lg font-medium">Female</h3>
            <p className="text-2xl font-bold text-purple-600">{businessCategories?.population_sums['Female Population Sum']}</p>
          </div>
        </div>
      </div>

    
      {/* <Map center={{ lat: 13.0827, lng: 80.2707 }} /> */}
      <div  style={{ width: "100%", height: "900px" }}>
      {mapHTML === "" ? <div>MAP is loading</div> :
      <div
      dangerouslySetInnerHTML={{ __html: mapHTML }}
      style={{ width: "100%", height: "300px" }}
    />
}
</div>
      <div className="grid grid-cols-2 gap-6 mt-8">
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Running Business</h3>
            <p className="text-3xl font-bold text-indigo-600">{businessCategories?.business_categories_area.length}</p>
            <div className="grid grid-cols-4 gap-4 mt-4">
          

                {
                  businessCategories && businessCategories?.business_categories_area.map((data,i) => {
                    return (<div key={i} className="text-center p-3 bg-gray-50 rounded-lg">
                      <p className="text-sm text-gray-600">{data["Business Category"]}</p>
                    </div>)
                  })
                }
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Opportunities</h3>
            <p className="text-3xl font-bold text-green-600">{businessCategories?.missing_categories.length}</p>
            <div className="grid grid-cols-4 gap-4 mt-4">
     

{
                  businessCategories && businessCategories?.missing_categories.map((data,i) => {
                    return (
                      <Link
                      to={`/category/${areaId}/${data === "Store" ? "Others" :data.replace('/','_') }/0/${businessCategories?.population_sums['Total Population Sum']}`}
                      className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-all"
                    >
                    <div key={i} className="text-center p-3 bg-gray-50 rounded-lg">
                      <p className="text-sm text-gray-600">{data}</p>
                    </div>
                    </Link>)
                  })
                }
            </div>
          </div>
        </div>

      <div className="bg-indigo-50 rounded-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Total Business: {businessCategories?.business_categories_area.length}
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {businessCategories?.business_categories_area.map((data) => {
return ( 
  <Link
    to={`/category/${areaId}/${data['Business Category']=== "Store" ? "Others" :data['Business Category'].replace('/','_')}/${data['Count']}/${businessCategories?.population_sums['Total Population Sum']}`}
    className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-all"
  >
    <div className="flex items-center justify-between">
      <div className="flex items-center">
        <div className="h-8 w-8 bg-indigo-500 mr-3 rounded-full" />
        <div>
          <h3 className="text-lg font-medium">{data["Business Category"]}</h3>
          <p className="text-2xl font-bold text-indigo-600">{data["Count"]}</p>
        </div>
      </div>
    </div>
  </Link>

)
        })

        }
 </div>      

        
      </div>
    </div>
  );
}
{/* 
  <Link
    to={`/category/${areaId}/hotels`}
    className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-all"
  >
    <div className="flex items-center justify-between">
      <div className="flex items-center">
        <div className="h-8 w-8 bg-blue-500 mr-3 rounded-full" />
        <div>
          <h3 className="text-lg font-medium">Hotel</h3>
          <p className="text-2xl font-bold text-blue-600">{AREA_DATA.categories.hotels}</p>
        </div>
      </div>
    </div>
  </Link>

  <Link
    to={`/category/${areaId}/parks`}
    className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-all"
  >
    <div className="flex items-center justify-between">
      <div className="flex items-center">
        <div className="h-8 w-8 bg-green-500 mr-3 rounded-full" />
        <div>
          <h3 className="text-lg font-medium">Parks</h3>
          <p className="text-2xl font-bold text-green-600">{AREA_DATA.categories.parks}</p>
        </div>
      </div>
    </div>
  </Link> */}