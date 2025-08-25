import React, { createContext, useContext, useState, useEffect } from 'react'
import { authService } from '../services/authService'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Check if user is already logged in on app start
  useEffect(() => {
    const initAuth = async () => {
      try {
        const token = localStorage.getItem('authToken')
        if (token) {
          const userData = await authService.getCurrentUser()
          setUser(userData)
        }
      } catch (error) {
        console.error('Auth initialization error:', error)
        localStorage.removeItem('authToken')
      } finally {
        setLoading(false)
      }
    }

    initAuth()
  }, [])

  const login = async (email, password, rememberMe = false) => {
    try {
      setError(null)
      const response = await authService.login(email, password)
      
      // Extract token and user from response
      const { access_token, user: userData } = response
      
      if (rememberMe) {
        localStorage.setItem('authToken', access_token)
      } else {
        sessionStorage.setItem('authToken', access_token)
      }
      
      setUser(userData)
      return { success: true }
    } catch (error) {
      setError(error.message || 'Login failed')
      return { success: false, error: error.message }
    }
  }

  const signup = async (userData) => {
    try {
      setError(null)
      const response = await authService.signup(userData)
      
      // Extract token and user from response
      const { access_token, user: newUser } = response
      
      localStorage.setItem('authToken', access_token)
      setUser(newUser)
      return { success: true }
    } catch (error) {
      setError(error.message || 'Signup failed')
      return { success: false, error: error.message }
    }
  }

  const logout = async () => {
    try {
      await authService.logout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      localStorage.removeItem('authToken')
      sessionStorage.removeItem('authToken')
      setUser(null)
      setError(null)
    }
  }

  const updateProfile = async (profileData) => {
    try {
      setError(null)
      const updatedUser = await authService.updateProfile(profileData)
      setUser(updatedUser)
      return { success: true }
    } catch (error) {
      setError(error.message || 'Profile update failed')
      return { success: false, error: error.message }
    }
  }

  const forgotPassword = async (email) => {
    try {
      setError(null)
      await authService.forgotPassword(email)
      return { success: true }
    } catch (error) {
      setError(error.message || 'Password reset failed')
      return { success: false, error: error.message }
    }
  }

  const resetPassword = async (token, newPassword) => {
    try {
      setError(null)
      await authService.resetPassword(token, newPassword)
      return { success: true }
    } catch (error) {
      setError(error.message || 'Password reset failed')
      return { success: false, error: error.message }
    }
  }

  const clearError = () => {
    setError(null)
  }

  const value = {
    user,
    loading,
    error,
    login,
    signup,
    logout,
    updateProfile,
    forgotPassword,
    resetPassword,
    clearError,
    isAuthenticated: !!user
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}
