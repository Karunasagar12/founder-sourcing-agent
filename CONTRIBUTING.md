# 🤝 Contributing Guidelines

> **Founder Sourcing Agent - Development Guidelines**

**Developed by:** [Karunasagar Mohansundar](https://github.com/Karunasagar12)

Thank you for your interest in contributing to the Founder Sourcing Agent! This document provides guidelines and best practices for contributing to the project.

---

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Communication](#communication)

---

## 🚀 Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Node.js 18+** (for frontend development)
- **Python 3.11+** (for backend development)
- **Git** (for version control)
- **Docker** (for containerization)
- **Google Cloud SDK** (for deployment)

### Initial Setup

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/founder-sourcing-agent.git
   cd founder-sourcing-agent
   ```

2. **Set up development environment**
   ```bash
   # Frontend setup
   cd frontend
   npm install
   
   # Backend setup
   cd ../backend
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   # Copy example files
   cp frontend/env.example frontend/.env
   cp backend/env.example backend/.env
   
   # Edit with your API keys
   # HARVEST_API_KEY, GOOGLE_GEMINI_API_KEY, etc.
   ```

4. **Start development servers**
   ```bash
   # Frontend (Terminal 1)
   cd frontend && npm run dev
   
   # Backend (Terminal 2)
   cd backend && uvicorn main:app --reload
   ```

---

## 🔄 Development Workflow

### Branch Strategy

We follow a **feature branch workflow**:

```
main (production)
├── develop (integration)
├── feature/authentication
├── feature/search-enhancement
├── bugfix/api-error-handling
└── hotfix/security-patch
```

### Branch Naming Convention

- **Feature branches**: `feature/descriptive-name`
- **Bug fixes**: `bugfix/issue-description`
- **Hotfixes**: `hotfix/critical-fix`
- **Documentation**: `docs/update-readme`

### Commit Message Format

Use **conventional commit messages**:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(auth): add JWT token refresh functionality
fix(search): resolve API rate limiting issue
docs(api): update endpoint documentation
test(backend): add authentication unit tests
```

---

## 📝 Code Standards

### Frontend (React/TypeScript)

#### Code Style
- Use **TypeScript** for type safety
- Follow **ESLint** and **Prettier** configurations
- Use **functional components** with hooks
- Implement **proper error boundaries**

#### Component Structure
```typescript
// Component template
import React from 'react';
import { ComponentProps } from './types';

interface ComponentProps {
  // Define props interface
}

export const Component: React.FC<ComponentProps> = ({ prop1, prop2 }) => {
  // Component logic
  
  return (
    // JSX
  );
};
```

#### State Management
- Use **React Context** for global state
- Use **local state** for component-specific data
- Implement **proper loading states**

### Backend (Python/FastAPI)

#### Code Style
- Follow **PEP 8** guidelines
- Use **type hints** for all functions
- Implement **proper error handling**
- Use **Pydantic models** for validation

#### Function Structure
```python
from typing import List, Optional
from pydantic import BaseModel

class SearchCriteria(BaseModel):
    """Search criteria model."""
    industry: Optional[str] = None
    years_of_experience: Optional[int] = None

async def search_founders(criteria: SearchCriteria) -> List[dict]:
    """
    Search for founders based on criteria.
    
    Args:
        criteria: Search criteria object
        
    Returns:
        List of candidate profiles
        
    Raises:
        ValidationError: If criteria is invalid
    """
    # Function implementation
    pass
```

#### Error Handling
```python
from fastapi import HTTPException

async def api_endpoint():
    try:
        # API logic
        return {"status": "success"}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

---

## 🧪 Testing Guidelines

### Frontend Testing

#### Unit Tests
- Test individual components
- Mock external dependencies
- Test user interactions
- Verify component rendering

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { SearchForm } from './SearchForm';

describe('SearchForm', () => {
  it('should submit search criteria', () => {
    const mockOnSearch = jest.fn();
    render(<SearchForm onSearch={mockOnSearch} />);
    
    fireEvent.click(screen.getByText('Search'));
    expect(mockOnSearch).toHaveBeenCalled();
  });
});
```

#### Integration Tests
- Test component interactions
- Test API integration
- Test routing functionality

### Backend Testing

#### Unit Tests
- Test individual functions
- Mock external API calls
- Test data validation
- Test error scenarios

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_search_endpoint():
    """Test search endpoint with valid criteria."""
    response = client.post("/search", json={
        "industry": "healthcare",
        "years_of_experience": 5
    })
    assert response.status_code == 200
    assert "candidates" in response.json()
```

#### API Tests
- Test all endpoints
- Test authentication
- Test error responses
- Test rate limiting

### Running Tests

```bash
# Frontend tests
cd frontend
npm test

# Backend tests
cd backend
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

---

## 🔀 Pull Request Process

### Before Submitting

1. **Ensure tests pass**
   ```bash
   # Frontend
   npm test
   npm run lint
   
   # Backend
   pytest tests/ -v
   black .
   flake8 .
   ```

2. **Update documentation**
   - Update README if needed
   - Add API documentation for new endpoints
   - Update inline code comments

3. **Check for conflicts**
   ```bash
   git fetch origin
   git rebase origin/main
   ```

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes

## Screenshots (if applicable)
Add screenshots for UI changes

## Additional Notes
Any additional information
```

### Review Process

1. **Automated Checks**
   - CI/CD pipeline runs tests
   - Code quality checks
   - Security scans

2. **Code Review**
   - At least one approval required
   - Address review comments
   - Update PR as needed

3. **Merge Process**
   - Squash commits if needed
   - Merge to main branch
   - Delete feature branch

---

## 🐛 Issue Reporting

### Bug Reports

Use the **bug report template**:

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Windows 10]
- Browser: [e.g., Chrome 120]
- Node.js: [e.g., 18.17.0]
- Python: [e.g., 3.11.0]

## Additional Context
Screenshots, logs, etc.
```

### Feature Requests

Use the **feature request template**:

```markdown
## Feature Description
Clear description of the feature

## Problem Statement
What problem does this solve?

## Proposed Solution
How should this be implemented?

## Alternative Solutions
Other approaches considered

## Additional Context
Screenshots, mockups, etc.
```

---

## 💬 Communication

### Communication Channels

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For general questions and ideas
- **Pull Request Comments**: For code review discussions

### Code Review Guidelines

#### For Reviewers
- Be constructive and respectful
- Focus on code quality and functionality
- Provide specific feedback
- Suggest improvements when possible

#### For Authors
- Respond to review comments promptly
- Address all feedback
- Ask for clarification if needed
- Update PR based on feedback

### Best Practices

1. **Be Respectful**
   - Use inclusive language
   - Be patient with newcomers
   - Provide constructive feedback

2. **Be Clear**
   - Write clear commit messages
   - Provide detailed PR descriptions
   - Include context in issues

3. **Be Responsive**
   - Respond to issues and PRs promptly
   - Keep discussions active
   - Update status regularly

---

## 🏆 Recognition

### Contributors

All contributors will be recognized in:

- **README.md** contributors section
- **GitHub contributors** page
- **Release notes** for significant contributions

### Contribution Levels

- **Bronze**: 1-5 contributions
- **Silver**: 6-15 contributions
- **Gold**: 16+ contributions
- **Platinum**: Major feature contributions

---

## 📚 Resources

### Documentation
- [Frontend README](frontend/README.md)
- [Backend README](backend/README.md)
- [API Documentation](docs/API.md)
- [Deployment Guide](deployment/README.md)

### External Resources
- [React Documentation](https://react.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Python Style Guide](https://peps.python.org/pep-0008/)

---

## 🆘 Getting Help

### Need Help?

- **Check existing issues** for similar problems
- **Search documentation** for solutions
- **Ask in discussions** for general questions
- **Create an issue** for bugs or feature requests

### Contact

- **Developer**: [Karunasagar Mohansundar](https://github.com/Karunasagar12)
- **Repository**: [Founder Sourcing Agent](https://github.com/Karunasagar12/founder-sourcing-agent)

---

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

*Thank you for contributing to the Founder Sourcing Agent! 🚀*
