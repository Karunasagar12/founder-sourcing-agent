import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Search, Users, BarChart3 } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import UserMenu from './user/UserMenu'

const Header = () => {
  const location = useLocation()
  const { isAuthenticated } = useAuth()

  const navItems = [
    { path: '/', label: 'Search', icon: Search },
    { path: '/results', label: 'Results', icon: Users },
  ]

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-4">
            {/* Modern Logo */}
            <Link to="/" className="flex items-center space-x-3 group">
              <div className="relative">
                {/* Main Logo Container */}
                <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-800 rounded-xl flex items-center justify-center shadow-lg relative overflow-hidden transition-all duration-300 group-hover:shadow-xl group-hover:scale-105">
                  {/* Network/Connection Lines */}
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="w-6 h-6 border-2 border-white/30 rounded-full relative">
                      {/* Connection dots */}
                      <div className="absolute -top-1 -left-1 w-2 h-2 bg-white rounded-full transition-all duration-300 group-hover:scale-110"></div>
                      <div className="absolute -top-1 -right-1 w-2 h-2 bg-white rounded-full transition-all duration-300 group-hover:scale-110"></div>
                      <div className="absolute -bottom-1 -left-1 w-2 h-2 bg-white rounded-full transition-all duration-300 group-hover:scale-110"></div>
                      <div className="absolute -bottom-1 -right-1 w-2 h-2 bg-white rounded-full transition-all duration-300 group-hover:scale-110"></div>
                    </div>
                  </div>
                  
                  {/* Central Search Icon */}
                  <div className="relative z-10 transition-transform duration-300 group-hover:scale-110">
                    <Search className="h-5 w-5 text-white" strokeWidth={2.5} />
                  </div>
                  
                  {/* Subtle glow effect */}
                  <div className="absolute inset-0 bg-gradient-to-br from-blue-400/20 to-transparent rounded-xl"></div>
                  
                  {/* Hover glow effect */}
                  <div className="absolute inset-0 bg-gradient-to-br from-blue-500/0 to-blue-700/0 rounded-xl transition-all duration-300 group-hover:from-blue-500/20 group-hover:to-blue-700/20"></div>
                </div>
              </div>
              
              {/* Logo Text */}
              <div className="flex flex-col">
                <h1 className="text-xl font-bold text-gray-900 leading-tight transition-colors duration-200 group-hover:text-blue-600">
                  Founder Sourcing
                  <span className="text-blue-600 group-hover:text-blue-700"> Agent</span>
                </h1>
                <p className="text-xs text-gray-500 font-medium -mt-1 transition-colors duration-200 group-hover:text-gray-600">
                  Developed by Karunasagar Mohansundar
                </p>
              </div>
            </Link>
          </div>

          <div className="flex items-center space-x-4">
            {/* Navigation */}
            {isAuthenticated && (
              <nav className="flex items-center space-x-1">
                {navItems.map((item) => {
                  const Icon = item.icon
                  const isActive = location.pathname === item.path
                  
                  return (
                    <Link
                      key={item.path}
                      to={item.path}
                      className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-200 ${
                        isActive
                          ? 'bg-primary-50 text-primary-700'
                          : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                      }`}
                    >
                      <Icon className="h-4 w-4" />
                      <span>{item.label}</span>
                    </Link>
                  )
                })}
              </nav>
            )}

            {/* User Menu or Auth Links */}
            {isAuthenticated ? (
              <UserMenu />
            ) : (
              <div className="flex items-center space-x-3">
                <Link
                  to="/login"
                  className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors duration-200"
                >
                  Sign in
                </Link>
                <Link
                  to="/signup"
                  className="btn-primary text-sm"
                >
                  Sign up
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
