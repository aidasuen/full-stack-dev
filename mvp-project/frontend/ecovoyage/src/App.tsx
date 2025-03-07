import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink, Navigate } from 'react-router-dom';
import { FaBars, FaTimes } from 'react-icons/fa';
import RoutePlanner from './components/RoutePlanner';
import Rewards from './components/Rewards';
import Login from './components/Login';
import Register from './components/Register';
import Home from './components/Home';
import Community from './components/Community';

const App: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return localStorage.getItem('isAuthenticated') === 'true';
  });

  useEffect(() => {
    localStorage.setItem('isAuthenticated', isAuthenticated.toString());
  }, [isAuthenticated]);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
  };

  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-green-50">
        {isAuthenticated && (
          <header className="bg-green-500 p-4 flex justify-between items-center">
            <h1 className="text-3xl text-white">EcoVoyage</h1>
            <button onClick={toggleMenu} className="text-white text-2xl focus:outline-none">
              {isMenuOpen ? <FaTimes /> : <FaBars />}
            </button>
          </header>
        )}

        <main className="flex-1 p-6">
          <Routes>
            <Route path="/login" element={<Login onLogin={handleLogin} />} />
            <Route path="/register" element={<Register />} />
            <Route
              path="/"
              element={isAuthenticated ? <Home /> : <Navigate to="/login" />}
            />
            <Route
              path="/routes"
              element={isAuthenticated ? <RoutePlanner /> : <Navigate to="/login" />}
            />
            <Route
              path="/community"
              element={isAuthenticated ? <Community /> : <Navigate to="/login" />}
            />
            <Route
              path="/rewards"
              element={isAuthenticated ? <Rewards /> : <Navigate to="/login" />}
            />
            <Route path="*" element={<Navigate to="/login" />} />
          </Routes>
        </main>

        {isAuthenticated && (
          <>
           
            {isMenuOpen && (
              <div
                className="fixed inset-0 bg-black bg-opacity-50 z-40"
                onClick={closeMenu} 
              />
            )}

            <nav
              className={`fixed top-0 right-0 h-full bg-green-500 text-white w-64 p-6 transform transition-transform duration-300 ease-in-out z-50 ${
                isMenuOpen ? 'translate-x-0' : 'translate-x-full'
              }`}
            >
              <ul className="flex flex-col space-y-6 mt-16">
                <li>
                  <NavLink
                    to="/"
                    className={({ isActive }) => (isActive ? 'text-green-200 font-bold' : 'hover:text-green-200')}
                    onClick={closeMenu} 
                  >
                    Главная
                  </NavLink>
                </li>
                <li>
                  <NavLink
                    to="/routes"
                    className={({ isActive }) => (isActive ? 'text-green-200 font-bold' : 'hover:text-green-200')}
                    onClick={closeMenu} 
                  >
                    Маршруты
                  </NavLink>
                </li>
                <li>
                  <NavLink
                    to="/community"
                    className={({ isActive }) => (isActive ? 'text-green-200 font-bold' : 'hover:text-green-200')}
                    onClick={closeMenu} 
                  >
                    Сообщество
                  </NavLink>
                </li>
                <li>
                  <NavLink
                    to="/rewards"
                    className={({ isActive }) => (isActive ? 'text-green-200 font-bold' : 'hover:text-green-200')}
                    onClick={closeMenu} 
                  >
                    Награды
                  </NavLink>
                </li>
                <li>
                  <button onClick={handleLogout} className="text-white hover:text-green-200">
                    Выход
                  </button>
                </li>
              </ul>
            </nav>
          </>
        )}
      </div>
    </Router>
  );
};

export default App;