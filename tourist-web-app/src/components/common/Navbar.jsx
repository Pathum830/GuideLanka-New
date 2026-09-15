import { useContext, useState, useEffect } from 'react'; 
import { Link, useLocation } from 'react-router-dom';
import { Compass, ArrowRight, LogIn, Menu, X } from 'lucide-react'; 
import { AuthContext } from '../../context/AuthContext';
import LoginModal from '../auth/LoginModal'; 

export default function Navbar() {
  const { user } = useContext(AuthContext);
  const location = useLocation();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const getLinkClass = (path) => {
    const isActive = location.pathname === path;
    return `transition ${
      isActive 
        ? 'text-green-700 font-bold' 
        : 'text-gray-600 hover:text-green-700 font-semibold'
    }`;
  };

  const getMobileLinkClass = (path) => {
    const isActive = location.pathname === path;
    return `text-lg py-2 border-b border-gray-100 transition ${
      isActive 
        ? 'text-green-700 font-bold' 
        : 'text-gray-700 hover:text-green-700 font-semibold'
    }`;
  };

  useEffect(() => {
    if (user && isModalOpen) {
      const timer = setTimeout(() => setIsModalOpen(false), 0);
      return () => clearTimeout(timer);
    }
  }, [user, isModalOpen]);

  return (
    <>
      <nav className="flex items-center justify-between px-6 py-4 bg-white/90 backdrop-blur-md shadow-sm fixed w-full z-50">
        <Link to="/" onClick={() => setIsMobileMenuOpen(false)} className="flex items-center space-x-2 text-green-700 cursor-pointer">
          <Compass size={32} />
          <span className="text-2xl font-extrabold tracking-tight">GuideLanka</span>
        </Link>
        
        <div className="hidden md:flex space-x-8 items-center">
          <Link to="/" className={getLinkClass('/')}>Home</Link>
          <Link to="/about" className={getLinkClass('/about')}>About</Link>
          <Link to="/rules" className={getLinkClass('/rules')}>Park Rules</Link>
          <Link to="/drivers" className={getLinkClass('/drivers')}>Drivers</Link>
          <Link to="/gallery" className={getLinkClass('/gallery')}>Gallery</Link>
          <Link to="/map" className={getLinkClass('/map')}>Live Map</Link> 
        </div>
        
        <div className="hidden md:flex items-center space-x-4">
          {user ? (
            <>
              <Link 
                to="/profile" 
                className="flex items-center space-x-2 bg-gray-50 hover:bg-green-50 hover:border-green-300 transition cursor-pointer px-3 py-1.5 rounded-full border border-gray-200"
                title="View Profile"
              >
                <img src={user.photoURL} alt="User" className="w-8 h-8 rounded-full" />
                <span className="font-bold text-sm text-gray-800">{user.displayName?.split(' ')[0]}</span>
              </Link>
            </>
          ) : (
            <>
              <button 
                onClick={() => setIsModalOpen(true)}
                className="text-gray-600 hover:text-green-700 font-bold flex items-center transition px-2"
              >
                <LogIn size={18} className="mr-2" /> Log In
              </button>

              <Link to="/booking" className="bg-green-700 text-white px-6 py-2.5 rounded-full font-bold hover:bg-green-800 transition flex items-center">
                Book Safari <ArrowRight className="ml-2" size={18} />
              </Link>
            </>
          )}
        </div>

        <div className="flex md:hidden items-center">
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="p-2 text-gray-600 hover:text-green-700 transition focus:outline-none"
            aria-label="Toggle mobile menu"
          >
            {isMobileMenuOpen ? <X size={26} /> : <Menu size={26} />}
          </button>
        </div>

        {isMobileMenuOpen && (
          <div className="md:hidden absolute top-full left-0 w-full bg-white/95 backdrop-blur-md border-b border-gray-200 shadow-lg py-6 px-6 z-40 flex flex-col space-y-6 animate-in fade-in slide-in-from-top-4 duration-200">
            <div className="flex flex-col space-y-4">
              <Link to="/" onClick={() => setIsMobileMenuOpen(false)} className={getMobileLinkClass('/')}>Home</Link>
              <Link to="/about" onClick={() => setIsMobileMenuOpen(false)} className={getMobileLinkClass('/about')}>About</Link>
              <Link to="/rules" onClick={() => setIsMobileMenuOpen(false)} className={getMobileLinkClass('/rules')}>Park Rules</Link>
              <Link to="/drivers" onClick={() => setIsMobileMenuOpen(false)} className={getMobileLinkClass('/drivers')}>Drivers</Link>
              <Link to="/gallery" onClick={() => setIsMobileMenuOpen(false)} className={getMobileLinkClass('/gallery')}>Gallery</Link>
              <Link to="/map" onClick={() => setIsMobileMenuOpen(false)} className={getMobileLinkClass('/map')}>Live Map</Link>
            </div>
            
            <div className="pt-4 border-t border-gray-100 flex flex-col space-y-4">
              {user ? (
                <div className="flex items-center justify-center w-full">
                  <Link 
                    to="/profile" 
                    onClick={() => setIsMobileMenuOpen(false)}
                    className="flex items-center justify-center space-x-3 bg-gray-50 hover:bg-green-50 hover:border-green-300 transition cursor-pointer px-4 py-2.5 rounded-full border border-gray-200 w-full"
                    title="View Profile"
                  >
                    <img src={user.photoURL} alt="User" className="w-9 h-9 rounded-full" />
                    <span className="font-bold text-gray-800">{user.displayName}</span>
                  </Link>
                </div>
              ) : (
                <div className="flex flex-col space-y-3">
                  <button 
                    onClick={() => { setIsModalOpen(true); setIsMobileMenuOpen(false); }}
                    className="w-full flex items-center justify-center bg-gray-50 text-gray-700 hover:text-green-700 font-bold py-3 rounded-xl border border-gray-200 transition"
                  >
                    <LogIn size={18} className="mr-2" /> Log In
                  </button>
                  <Link 
                    to="/booking" 
                    onClick={() => setIsMobileMenuOpen(false)} 
                    className="w-full bg-green-700 text-white py-3 rounded-xl font-bold hover:bg-green-800 transition flex items-center justify-center"
                  >
                    Book Safari <ArrowRight className="ml-2" size={18} />
                  </Link>
                </div>
              )}
            </div>
          </div>
        )}
      </nav>

      <LoginModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </>
  );
}