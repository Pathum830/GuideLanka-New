import { useState } from 'react';
import { 
  Camera, 
  Search, 
  Filter, 
  X,
  Eye,
  Maximize2,
  Share2
} from 'lucide-react';

const SHOWCASE_PHOTOS = [
  {
    id: 's1',
    title: 'Majestic Sri Lankan Elephant',
    category: 'Wildlife',
    tag: 'Elephant',
    image: 'https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?q=80&w=1032&auto=format&fit=crop',
    description: 'An adult male elephant wading through the waters of a lake during the golden hour in Yala National Park.'
  },
  {
    id: 's2',
    title: 'Leopard in the Scrublands',
    category: 'Wildlife',
    tag: 'Leopard',
    image: 'https://images.unsplash.com/photo-1456926631375-92c8ce872def?q=80&w=1200&auto=format&fit=crop',
    description: 'A Sri Lankan Leopard stealthily traversing dry forest paths. Yala is renowned for having one of the highest leopard densities in the world.'
  },
  {
    id: 's3',
    title: 'Jeep Safari Adventure',
    category: 'Safari Life',
    tag: 'Safari',
    image: 'https://images.unsplash.com/photo-1516426122078-c23e76319801?q=80&w=1200&auto=format&fit=crop',
    description: 'Custom-built safari jeeps trekking on red-dirt tracks, surrounded by dense dry woodlands and active wildlife.'
  },
  {
    id: 's4',
    title: 'Dancing Blue Peafowl',
    category: 'Wildlife',
    tag: 'Peacock',
    image: 'https://images.unsplash.com/photo-1536514900905-0d5511b9d489?fm=jpg&q=60&w=3000&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cGVhY29ja3N8ZW58MHx8MHx8fDA%3D',
    description: 'A male Indian Peacock displaying its vibrant, iridescent blue-green train feathers to attract attention.'
  },
  {
    id: 's5',
    title: 'Patanangala Beach Coastline',
    category: 'Landscapes',
    tag: 'Scenic',
    image: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1200&auto=format&fit=crop',
    description: 'Where the wilderness meets the Indian Ocean. The scenic coastline and dramatic rock formations at Patanangala, Yala.'
  },
  {
    id: 's6',
    title: 'Grasslands Spotted Deer',
    category: 'Wildlife',
    tag: 'Deer',
    image: 'https://images.unsplash.com/photo-1508138221679-760a23a2285b?q=80&w=1200&auto=format&fit=crop',
    description: 'A peaceful herd of axis deer (spotted deer) grazing in the wide savannah plains during the early morning hours.'
  }
];

export default function Gallery() {
  const [searchTerm, setSearchTerm] = useState('');
  const [showcaseCategory, setShowcaseCategory] = useState('All');
  const [activeLightboxImage, setActiveLightboxImage] = useState(null);

  const showcaseCategories = ['All', 'Wildlife', 'Landscapes', 'Safari Life'];

  const handleShare = async (title, text) => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: title,
          text: text,
          url: window.location.href,
        });
      } catch (err) {
        console.error('Error sharing:', err);
      }
    } else {
      alert(`URL Copied! - Shared: ${title}`);
    }
  };

  const filteredShowcase = SHOWCASE_PHOTOS.filter(photo => {
    const matchesSearch = (photo.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          photo.description.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesCategory = showcaseCategory === 'All' || photo.category === showcaseCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="pt-24 pb-16 min-h-screen bg-gray-50/50 font-sans">
      
      <div className="relative bg-green-950 py-16 md:py-20 text-white overflow-hidden mb-8">
        <div className="absolute inset-0 opacity-25 bg-[url('https://images.unsplash.com/photo-1549366021-9f761d450615?q=80&w=2000&auto=format&fit=crop')] bg-cover bg-center mix-blend-overlay"></div>
        <div className="absolute inset-0 bg-linear-to-t from-green-950 via-green-900/60 to-transparent"></div>
        
        <div className="container mx-auto px-4 max-w-6xl relative z-10 text-center space-y-4">
          <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-md px-4 py-1.5 rounded-full text-xs font-black uppercase tracking-widest text-green-300 border border-white/10 shadow-inner">
            <Camera size={14} />
            Official Yala Gallery
          </div>
          <h1 className="text-4xl md:text-5xl font-black tracking-tight drop-shadow-md">
            Yala Photo Showcase
          </h1>
          <p className="text-green-100/90 text-sm md:text-base max-w-xl mx-auto font-medium">
            Explore a curated collection of high-definition wildlife, scenic landscapes, and safari experiences from Yala National Park.
          </p>
        </div>
      </div>

      <div className="container mx-auto px-4 max-w-6xl space-y-8">
        
        <div className="bg-white p-5 rounded-3xl border border-gray-200 shadow-sm flex flex-col md:flex-row items-center justify-between gap-4">
          
          <div className="relative w-full md:max-w-xs">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400" size={17} />
            <input
              type="text"
              placeholder="Search photo showcase..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 bg-gray-55 bg-gray-50 border border-gray-300 text-sm font-semibold text-gray-700 placeholder-gray-400 rounded-2xl focus:border-green-600 focus:outline-none transition"
            />
            {searchTerm && (
              <button 
                onClick={() => setSearchTerm('')}
                className="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-650"
              >
                <X size={15} />
              </button>
            )}
          </div>

          <div className="flex items-center gap-2 overflow-x-auto w-full md:w-auto pb-2 md:pb-0 no-scrollbar">
            <div className="flex items-center text-xs font-black text-gray-400 uppercase tracking-wider mr-2 shrink-0">
              <Filter size={14} className="mr-1" /> Categories:
            </div>
            {showcaseCategories.map((cat) => (
              <button
                key={cat}
                onClick={() => setShowcaseCategory(cat)}
                className={`px-4 py-2.5 rounded-xl text-xs font-extrabold tracking-wide border transition shrink-0 cursor-pointer ${
                  showcaseCategory === cat
                    ? 'bg-green-700 text-white border-green-700 shadow-xs'
                    : 'bg-white text-gray-600 border-gray-200 hover:bg-gray-50 hover:border-gray-300'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

        </div>

        {filteredShowcase.length === 0 ? (
          <div className="bg-white rounded-3xl border border-gray-200 p-16 text-center space-y-4">
            <h3 className="text-xl font-bold text-gray-800">No Showcase Photos Found</h3>
            <p className="text-sm text-gray-500 max-w-sm mx-auto">
              No Yala photos match your search terms or category selection.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {filteredShowcase.map((photo) => (
              <div 
                key={photo.id}
                onClick={() => setActiveLightboxImage(photo)}
                className="group bg-white rounded-3xl border border-gray-200 overflow-hidden shadow-sm hover:shadow-xl hover:-translate-y-1 transition duration-300 flex flex-col cursor-pointer"
              >
                <div className="relative h-64 overflow-hidden bg-gray-200">
                  <img 
                    src={photo.image} 
                    alt={photo.title} 
                    className="w-full h-full object-cover group-hover:scale-105 transition duration-500"
                    loading="lazy"
                  />
                  
                  <div className="absolute inset-0 bg-black/35 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                    <div className="bg-white p-3 rounded-2xl shadow-lg text-green-700 transform translate-y-3 group-hover:translate-y-0 transition duration-300">
                      <Maximize2 size={18} />
                    </div>
                  </div>
                  
                  <span className="absolute top-4 left-4 px-3 py-1 rounded-xl text-xs font-black uppercase tracking-wider border border-white/20 bg-green-900/85 backdrop-blur-md text-white shadow-xs">
                    {photo.category}
                  </span>
                </div>

                <div className="p-6 flex-1 flex flex-col justify-between">
                  <div>
                    <h3 className="text-lg font-black text-gray-800 mb-2 group-hover:text-green-700 transition-colors">
                      {photo.title}
                    </h3>
                    <p className="text-gray-500 text-xs leading-relaxed font-semibold">
                      {photo.description}
                    </p>
                  </div>
                  
                  <div className="mt-4 pt-4 border-t border-gray-100 flex justify-between items-center text-xs font-bold text-gray-400">
                    <span>Click photo to expand</span>
                    <span className="text-green-700 flex items-center gap-1 font-black">
                      View Details <Eye size={13} />
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

      </div>

      {activeLightboxImage && (
        <div className="fixed inset-0 z-50 bg-black/90 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in">
          
          <button 
            onClick={() => setActiveLightboxImage(null)}
            className="absolute top-6 right-6 p-3 rounded-full bg-white/10 hover:bg-white/20 text-white transition cursor-pointer hover:scale-105"
          >
            <X size={20} />
          </button>

          <div className="max-w-4xl w-full bg-white rounded-3xl overflow-hidden shadow-2xl flex flex-col md:flex-row max-h-[85vh] animate-scale-up">
            
            <div className="flex-1 bg-black flex items-center justify-center overflow-hidden min-h-[300px] md:min-h-[500px]">
              <img 
                src={activeLightboxImage.image} 
                alt={activeLightboxImage.title} 
                className="w-full h-full object-contain max-h-[50vh] md:max-h-[80vh]"
              />
            </div>

            <div className="w-full md:w-80 p-6 md:p-8 flex flex-col justify-between bg-white shrink-0">
              <div className="space-y-4">
                <span className="inline-block px-3 py-1 rounded-xl text-[10px] font-black uppercase tracking-wider border border-green-200 bg-green-50 text-green-700">
                  {activeLightboxImage.category}
                </span>
                <h2 className="text-2xl font-black text-gray-800 leading-tight">
                  {activeLightboxImage.title}
                </h2>
                <p className="text-gray-500 text-sm leading-relaxed font-semibold">
                  {activeLightboxImage.description}
                </p>
              </div>

              <div className="mt-8 pt-6 border-t border-gray-100 flex items-center gap-3">
                <button
                  onClick={() => handleShare(
                    activeLightboxImage.title,
                    activeLightboxImage.description
                  )}
                  className="flex-1 bg-green-700 hover:bg-green-800 text-white font-extrabold py-3.5 px-4 rounded-2xl transition duration-200 cursor-pointer shadow-md shadow-green-700/10 active:scale-95 flex items-center justify-center gap-2 text-xs"
                >
                  <Share2 size={14} />
                  Share Photo
                </button>
                <button 
                  onClick={() => setActiveLightboxImage(null)}
                  className="bg-gray-100 hover:bg-gray-200 text-gray-600 font-bold py-3.5 px-5 rounded-2xl transition cursor-pointer text-xs"
                >
                  Close
                </button>
              </div>
            </div>

          </div>

        </div>
      )}
      
    </div>
  );
}
