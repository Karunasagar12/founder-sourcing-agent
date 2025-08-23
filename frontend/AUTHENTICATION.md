# Authentication System Documentation

## Overview

This document describes the professional authentication system implemented for the Founder Sourcing Agent CRM interface. The system provides secure user authentication, profile management, and protected routes.

## Features

### ✅ Authentication Interface
- Professional login/signup forms matching existing design system
- Email/password authentication with comprehensive validation
- Social login options (Google/LinkedIn) for founder audience
- Password strength indicators and forgot password flow
- Loading states and error handling with consistent styling

### ✅ User Management System
- User profile components and management
- Authentication state management with React Context
- Protected route wrapper for search functionality
- User menu with profile/logout options in existing header
- Session persistence and automatic login

### ✅ Navigation Integration
- Updated header component with authentication states
- User avatar and dropdown menu integration
- Seamless transition between authenticated/unauthenticated states
- Breadcrumb and navigation consistency

### ✅ Security and UX
- Form validation matching existing form styling
- JWT token handling and secure storage
- Auto-redirect after login to intended page
- Remember me functionality and session management
- Consistent error messaging and user feedback

## Architecture

### File Structure
```
frontend/src/
├── components/
│   ├── auth/
│   │   ├── LoginForm.jsx (login interface)
│   │   ├── SignupForm.jsx (registration interface)
│   │   └── ProtectedRoute.jsx (route protection)
│   ├── user/
│   │   ├── UserMenu.jsx (header dropdown)
│   └── [existing components remain unchanged]
├── pages/
│   ├── auth/
│   │   ├── Login.jsx (login page)
│   │   ├── Signup.jsx (registration page)
│   │   └── ForgotPassword.jsx (password reset)
│   ├── user/
│   │   └── Profile.jsx (user profile page)
│   └── [existing pages remain unchanged]
├── contexts/
│   └── AuthContext.jsx (authentication state management)
├── services/
│   └── authService.js (authentication API calls)
└── utils/
    └── auth.js (auth utilities and validation)
```

### Key Components

#### AuthContext.jsx
- Central authentication state management
- Provides login, signup, logout, and profile update functions
- Handles token storage and session management
- Automatic token refresh and error handling

#### ProtectedRoute.jsx
- Route protection wrapper component
- Redirects unauthenticated users to login
- Preserves intended destination for post-login redirect
- Loading states during authentication checks

#### UserMenu.jsx
- User avatar and dropdown menu in header
- Profile, settings, and logout options
- Responsive design with mobile considerations
- Smooth animations and interactions

## Authentication Flow

### 1. User Registration
1. User visits `/signup` page
2. Fills out comprehensive registration form with validation
3. Password strength indicator provides real-time feedback
4. Form validates all fields before submission
5. Success redirects to main application

### 2. User Login
1. User visits `/login` page (or redirected from protected route)
2. Enters email/password with validation
3. Optional "Remember me" for persistent sessions
4. Social login options available
5. Success redirects to intended page or dashboard

### 3. Protected Routes
1. Unauthenticated users accessing protected routes redirected to login
2. Original destination preserved for post-login redirect
3. Loading states shown during authentication checks
4. Seamless user experience with clear feedback

### 4. Session Management
1. JWT tokens stored securely (localStorage/sessionStorage)
2. Automatic token refresh handling
3. Token expiration detection and logout
4. Remember me functionality for persistent sessions

## API Integration

### Authentication Endpoints
- `POST /auth/login` - User login
- `POST /auth/signup` - User registration
- `POST /auth/logout` - User logout
- `GET /auth/me` - Get current user data
- `PUT /auth/profile` - Update user profile
- `POST /auth/forgot-password` - Request password reset
- `POST /auth/reset-password` - Reset password with token

### Request/Response Format
```javascript
// Login Request
{
  "email": "user@example.com",
  "password": "securePassword123"
}

// Login Response
{
  "user": {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "user@example.com",
    "company": "Tech Corp"
  },
  "token": "jwt_token_here"
}
```

## Security Features

### Token Management
- JWT tokens for stateless authentication
- Secure token storage with expiration handling
- Automatic token refresh mechanism
- Token validation on protected routes

### Form Validation
- Client-side validation for immediate feedback
- Server-side validation for security
- Password strength requirements
- Email format validation
- Required field validation

### Error Handling
- Comprehensive error messages
- User-friendly error display
- Network error handling
- Validation error feedback

## Styling and UX

### Design System Integration
- Consistent with existing Tailwind CSS classes
- Matches current color scheme and typography
- Responsive design for all screen sizes
- Smooth animations and transitions

### User Experience
- Loading states for all async operations
- Success/error feedback messages
- Intuitive form layouts and validation
- Accessible form elements and labels

## Configuration

### Environment Variables
```bash
# API Configuration
VITE_API_URL=http://localhost:8000

# Authentication Configuration
VITE_AUTH_ENABLED=true

# Social Login (Optional)
VITE_GOOGLE_CLIENT_ID=your_google_client_id
VITE_LINKEDIN_CLIENT_ID=your_linkedin_client_id
```

### Dependencies
```json
{
  "axios": "^1.3.0",
  "jwt-decode": "^4.0.0",
  "react-router-dom": "^6.8.0"
}
```

## Usage Examples

### Using AuthContext
```javascript
import { useAuth } from '../contexts/AuthContext'

const MyComponent = () => {
  const { user, login, logout, isAuthenticated } = useAuth()
  
  const handleLogin = async () => {
    const result = await login(email, password)
    if (result.success) {
      // Redirect or show success message
    }
  }
  
  return (
    <div>
      {isAuthenticated ? (
        <p>Welcome, {user.first_name}!</p>
      ) : (
        <button onClick={handleLogin}>Login</button>
      )}
    </div>
  )
}
```

### Protected Route Usage
```javascript
import ProtectedRoute from './components/auth/ProtectedRoute'

<Route path="/dashboard" element={
  <ProtectedRoute>
    <Dashboard />
  </ProtectedRoute>
} />
```

## Future Enhancements

### Planned Features
- Two-factor authentication (2FA)
- Email verification flow
- Advanced password policies
- User roles and permissions
- Audit logging
- Session management dashboard

### Social Login Integration
- Google OAuth implementation
- LinkedIn OAuth implementation
- Additional social providers
- Profile data synchronization

## Testing

### Manual Testing Checklist
- [ ] User registration with valid data
- [ ] User registration with invalid data
- [ ] User login with valid credentials
- [ ] User login with invalid credentials
- [ ] Password reset flow
- [ ] Protected route access
- [ ] Session persistence
- [ ] Logout functionality
- [ ] Profile update
- [ ] Error handling scenarios

### Automated Testing
- Unit tests for auth utilities
- Integration tests for auth service
- Component tests for auth forms
- E2E tests for authentication flow

## Troubleshooting

### Common Issues
1. **Token not persisting**: Check localStorage/sessionStorage permissions
2. **API calls failing**: Verify VITE_API_URL configuration
3. **Redirect loops**: Check ProtectedRoute implementation
4. **Form validation errors**: Verify validation functions

### Debug Mode
Enable debug logging by setting `VITE_DEBUG=true` in environment variables.

## Support

For issues or questions regarding the authentication system, please refer to:
- API documentation for backend integration
- React Router documentation for routing
- Tailwind CSS documentation for styling
- JWT documentation for token handling
