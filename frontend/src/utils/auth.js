// Email validation
export const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

// Password strength validation
export const validatePassword = (password) => {
  const minLength = 8
  const hasUpperCase = /[A-Z]/.test(password)
  const hasLowerCase = /[a-z]/.test(password)
  const hasNumbers = /\d/.test(password)
  const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password)

  const errors = []
  
  if (password.length < minLength) {
    errors.push(`At least ${minLength} characters`)
  }
  if (!hasUpperCase) {
    errors.push('At least one uppercase letter')
  }
  if (!hasLowerCase) {
    errors.push('At least one lowercase letter')
  }
  if (!hasNumbers) {
    errors.push('At least one number')
  }
  if (!hasSpecialChar) {
    errors.push('At least one special character')
  }

  return {
    isValid: errors.length === 0,
    errors,
    strength: getPasswordStrength(password)
  }
}

// Get password strength score (0-4)
export const getPasswordStrength = (password) => {
  let score = 0
  
  if (password.length >= 8) score++
  if (/[A-Z]/.test(password)) score++
  if (/[a-z]/.test(password)) score++
  if (/\d/.test(password)) score++
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score++
  
  return score
}

// Get password strength label
export const getPasswordStrengthLabel = (strength) => {
  switch (strength) {
    case 0:
    case 1:
      return { label: 'Very Weak', color: 'text-red-600', bgColor: 'bg-red-100' }
    case 2:
      return { label: 'Weak', color: 'text-orange-600', bgColor: 'bg-orange-100' }
    case 3:
      return { label: 'Fair', color: 'text-yellow-600', bgColor: 'bg-yellow-100' }
    case 4:
      return { label: 'Good', color: 'text-blue-600', bgColor: 'bg-blue-100' }
    case 5:
      return { label: 'Strong', color: 'text-green-600', bgColor: 'bg-green-100' }
    default:
      return { label: 'Very Weak', color: 'text-red-600', bgColor: 'bg-red-100' }
  }
}

// Name validation
export const validateName = (name) => {
  return name.trim().length >= 2 && /^[a-zA-Z\s]+$/.test(name)
}

// Company validation
export const validateCompany = (company) => {
  return company.trim().length >= 2
}

// Get user initials for avatar
export const getUserInitials = (firstName, lastName) => {
  const first = firstName ? firstName.charAt(0).toUpperCase() : ''
  const last = lastName ? lastName.charAt(0).toUpperCase() : ''
  return first + last
}

// Format user name
export const formatUserName = (firstName, lastName) => {
  if (!firstName && !lastName) return 'User'
  return `${firstName || ''} ${lastName || ''}`.trim()
}

// Check if token is expired
export const isTokenExpired = (token) => {
  if (!token) return true
  
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.exp * 1000 < Date.now()
  } catch (error) {
    return true
  }
}

// Get token expiration time
export const getTokenExpiration = (token) => {
  if (!token) return null
  
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return new Date(payload.exp * 1000)
  } catch (error) {
    return null
  }
}

// Generate random avatar color
export const getAvatarColor = (name) => {
  const colors = [
    'bg-red-500',
    'bg-blue-500',
    'bg-green-500',
    'bg-yellow-500',
    'bg-purple-500',
    'bg-pink-500',
    'bg-indigo-500',
    'bg-teal-500'
  ]
  
  let hash = 0
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash)
  }
  
  return colors[Math.abs(hash) % colors.length]
}

// Validate form data
export const validateFormData = (data, fields) => {
  const errors = {}
  
  fields.forEach(field => {
    const { name, required, validator, message } = field
    
    if (required && (!data[name] || data[name].toString().trim() === '')) {
      errors[name] = message || `${name} is required`
    } else if (validator && data[name]) {
      const validation = validator(data[name])
      if (!validation.isValid) {
        errors[name] = validation.errors[0] || message || `${name} is invalid`
      }
    }
  })
  
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  }
}
