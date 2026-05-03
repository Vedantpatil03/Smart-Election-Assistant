import React from 'react';
import { NavLink } from 'react-router-dom';
import { FiLogOut } from 'react-icons/fi';

const Navbar = ({ loggedInUser, onLogout }) => {
  return (
    <nav className="sticky top-0 z-50 bg-white rounded-2xl shadow-md mx-4 mt-3">
      <div className="max-w-7xl mx-auto px-6 py-3 flex items-center justify-between">
        
        {/* LEFT SECTION - LOGO & BRANDING */}
        <div className="flex items-center gap-3 min-w-fit">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center">
            <span className="text-white font-bold text-sm">SEA</span>
          </div>
          <div className="hidden sm:block">
            <p className="text-sm font-bold text-gray-900">Smart Election Assistant</p>
            <p className="text-xs text-gray-500">Voter support dashboard</p>
          </div>
        </div>

        {/* CENTER SECTION - NAVIGATION LINKS */}
        <div className="hidden md:flex items-center gap-1 flex-1 justify-center mx-8">
          <NavLink
            to="/home"
            className={({ isActive }) =>
              `px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-700 hover:bg-gray-100'
              }`
            }
          >
            Home
          </NavLink>

          <NavLink
            to="/guide"
            className={({ isActive }) =>
              `px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-700 hover:bg-gray-100'
              }`
            }
          >
            Guide
          </NavLink>

          <NavLink
            to="/timeline"
            className={({ isActive }) =>
              `px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-700 hover:bg-gray-100'
              }`
            }
          >
            Timeline
          </NavLink>

          <NavLink
            to="/faq"
            className={({ isActive }) =>
              `px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-700 hover:bg-gray-100'
              }`
            }
          >
            FAQ
          </NavLink>

          <NavLink
            to="/quiz"
            className={({ isActive }) =>
              `px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-700 hover:bg-gray-100'
              }`
            }
          >
            Quiz
          </NavLink>

          <NavLink
            to="/chat"
            className={({ isActive }) =>
              `px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-700 hover:bg-gray-100'
              }`
            }
          >
            Chat
          </NavLink>
        </div>

        {/* RIGHT SECTION - USER INFO & LOGOUT */}
        <div className="flex items-center gap-4">
          <div className="hidden sm:block text-right">
            <p className="text-sm font-semibold text-gray-900">
              {loggedInUser?.name || 'Guest'}
            </p>
            <p className="text-xs text-gray-500">{loggedInUser?.voterId || ''}</p>
          </div>

          <button
            onClick={onLogout}
            className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors duration-200"
          >
            <FiLogOut className="w-4 h-4" />
            <span className="hidden sm:inline">Logout</span>
          </button>
        </div>
      </div>

      {/* MOBILE NAVIGATION */}
      <div className="md:hidden border-t border-gray-200 px-6 py-3 flex gap-2 overflow-x-auto">
        <NavLink
          to="/home"
          className={({ isActive }) =>
            `px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap transition-all duration-200 ${
              isActive
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700'
            }`
          }
        >
          Home
        </NavLink>
        <NavLink
          to="/guide"
          className={({ isActive }) =>
            `px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap transition-all duration-200 ${
              isActive
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700'
            }`
          }
        >
          Guide
        </NavLink>
        <NavLink
          to="/timeline"
          className={({ isActive }) =>
            `px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap transition-all duration-200 ${
              isActive
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700'
            }`
          }
        >
          Timeline
        </NavLink>
        <NavLink
          to="/faq"
          className={({ isActive }) =>
            `px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap transition-all duration-200 ${
              isActive
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700'
            }`
          }
        >
          FAQ
        </NavLink>
        <NavLink
          to="/quiz"
          className={({ isActive }) =>
            `px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap transition-all duration-200 ${
              isActive
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700'
            }`
          }
        >
          Quiz
        </NavLink>
        <NavLink
          to="/chat"
          className={({ isActive }) =>
            `px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap transition-all duration-200 ${
              isActive
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700'
            }`
          }
        >
          Chat
        </NavLink>
      </div>
    </nav>
  );
};

export default Navbar;
