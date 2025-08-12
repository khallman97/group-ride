# Development Guide

This guide provides detailed information for developers working on the Group Fitness App.

## 🏁 Getting Started

### Prerequisites
- **Docker** 20.0+ and **Docker Compose** 2.0+
- **AWS Account** with Cognito configured
- **Node.js** 18+ (for local frontend development)
- **Python** 3.11+ (for local backend development)

### First-Time Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd group-fitness-app
   ```

2. **Set up AWS Cognito:**
   ```bash
   # Run the setup script (if you have AWS CLI configured)
   chmod +x setup-cognito.sh
   ./setup-cognito.sh
   ```

3. **Configure environment:**
   ```bash
   cp env.example .env
   # Edit .env with your AWS credentials
   ```

4. **Start development environment:**
   ```bash
   docker-compose up -d
   docker-compose exec backend python create_tables.py
   ```

## 🏗️ Architecture Overview

### Backend (FastAPI)
- **Framework**: FastAPI with async support
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: AWS Cognito integration
- **API Documentation**: Automatic with OpenAPI/Swagger

### Frontend (React Native Web)
- **Framework**: React with TypeScript
- **Styling**: CSS with responsive design
- **State Management**: React Context API
- **Cross-Platform**: Web-first, mobile-ready

### Infrastructure
- **Local Development**: Docker Compose
- **Database**: PostgreSQL 15
- **Caching**: Redis 7
- **File Storage**: MinIO (S3-compatible)

## 🔧 Development Workflow

### Backend Development

#### Running Locally
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Access container
docker-compose exec backend bash

# Run database migrations
docker-compose exec backend python create_tables.py
```

#### Adding New Endpoints
1. **Create schema** in `backend/app/schemas/`
2. **Add database model** in `backend/app/models/`
3. **Implement service logic** in `backend/app/services/`
4. **Create router** in `backend/app/routers/`
5. **Register router** in `backend/app/main.py`

#### Database Changes
```bash
# Access database
docker-compose exec postgres psql -U dev_user -d group_fitness_dev

# View tables
\dt

# Query data
SELECT * FROM user_profiles;
```

### Frontend Development

#### Running Locally
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f frontend

# Install new package
docker-compose exec frontend npm install <package-name>

# Access container
docker-compose exec frontend sh
```

#### Adding New Components
1. **Create component** in `frontend/src/components/`
2. **Add TypeScript interfaces** for props
3. **Implement responsive styling**
4. **Add to parent component**
5. **Test on different screen sizes**

#### API Integration
```typescript
// 1. Add interface to api.ts
interface NewFeature {
  id: string;
  name: string;
}

// 2. Add API method
async getNewFeature(): Promise<NewFeature> {
  const response = await fetch(`${API_BASE_URL}/new-feature`, {
    headers: this.getAuthHeaders(),
  });
  return this.handleResponse<NewFeature>(response);
}

// 3. Use in component
const [feature, setFeature] = useState<NewFeature | null>(null);

useEffect(() => {
  const fetchFeature = async () => {
    try {
      const data = await apiService.getNewFeature();
      setFeature(data);
    } catch (error) {
      console.error('Failed to fetch feature:', error);
    }
  };
  fetchFeature();
}, []);
```

## 🧪 Testing

### Backend Testing
```bash
# Run tests (when implemented)
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov=app

# Test specific file
docker-compose exec backend pytest tests/test_auth.py
```

### Frontend Testing
```bash
# Run tests
docker-compose exec frontend npm test

# Run tests with coverage
docker-compose exec frontend npm test -- --coverage

# Run tests in CI mode
docker-compose exec frontend npm test -- --ci --watchAll=false
```

### Manual Testing
1. **Authentication Flow**:
   - Sign up → Email confirmation → Sign in
   - Test with invalid credentials
   - Test token refresh

2. **Onboarding Flow**:
   - Complete all 3 steps
   - Test validation
   - Test back/next navigation

3. **Responsive Design**:
   - Test on mobile (375px width)
   - Test on tablet (768px width)
   - Test on desktop (1200px+ width)

## 🐛 Debugging

### Common Issues

#### "Database connection failed"
```bash
# Check database status
docker-compose exec postgres pg_isready

# Restart database
docker-compose restart postgres

# Check logs
docker-compose logs postgres
```

#### "Frontend not loading"
```bash
# Check if frontend is running
docker-compose ps frontend

# Restart frontend
docker-compose restart frontend

# Check for JavaScript errors
docker-compose logs frontend
```

#### "AWS Cognito errors"
```bash
# Check environment variables
docker-compose exec backend python -c "
from app.config import get_settings
settings = get_settings()
print(f'Region: {settings.AWS_REGION}')
print(f'User Pool: {settings.COGNITO_USER_POOL_ID[:10]}...')
print(f'Client ID: {settings.COGNITO_CLIENT_ID[:10]}...')
"

# Test Cognito connection
aws cognito-idp describe-user-pool --user-pool-id YOUR_USER_POOL_ID
```

### Debug Tools

#### Backend Debugging
```python
# Add debug prints
import logging
logging.basicConfig(level=logging.DEBUG)

# Use debugger
import pdb; pdb.set_trace()

# Check FastAPI logs
# Visit http://localhost:8000/docs for API testing
```

#### Frontend Debugging
```typescript
// Browser DevTools
console.log('Debug info:', data);

// React DevTools extension
// Network tab for API calls
// Application tab for localStorage
```

## 📦 Deployment

### Local Development
Already configured - just run `docker-compose up -d`

### Production Checklist
- [ ] Update CORS origins in `backend/app/main.py`
- [ ] Set secure environment variables
- [ ] Configure production database
- [ ] Set up AWS services (RDS, S3, Cognito)
- [ ] Build optimized frontend
- [ ] Configure monitoring and logging

### Environment Variables for Production
```bash
# Backend
DATABASE_URL=postgresql://user:pass@rds-endpoint:5432/dbname
REDIS_URL=redis://elasticache-endpoint:6379
S3_ENDPOINT=  # Leave empty for AWS S3
S3_BUCKET=your-production-bucket
AWS_REGION=us-east-1
COGNITO_USER_POOL_ID=us-east-1_xxxxxxxxx
COGNITO_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxx

# Frontend
REACT_APP_API_URL=https://your-api-domain.com
```

## 🔒 Security Considerations

### Authentication
- JWT tokens are stored in localStorage (consider httpOnly cookies for production)
- AWS Cognito handles password security and token refresh
- All API endpoints are protected except auth endpoints

### Data Privacy
- User emails are stored for authentication only
- Location data is stored as lat/lng but not tracked
- No personal fitness data is collected

### Environment Security
- Never commit `.env` files
- Use AWS IAM roles in production instead of access keys
- Regularly rotate AWS credentials

## 📚 Code Style

### Backend (Python)
- Follow PEP 8 style guide
- Use type hints for all functions
- Document functions with docstrings
- Use async/await for all endpoints

### Frontend (TypeScript)
- Use functional components with hooks
- Define interfaces for all props and data
- Use meaningful variable names
- Add comments for complex logic

### General
- Keep functions small and focused
- Use descriptive commit messages
- Add comments for business logic
- Update documentation when adding features

## 🚀 Performance

### Backend Optimization
- Database queries are optimized with proper indexing
- Use connection pooling for database
- Implement caching with Redis for expensive operations
- Use async endpoints for better concurrency

### Frontend Optimization
- Components are functional with React hooks
- Use React.memo for expensive components
- Lazy load images and large components
- Minimize bundle size with proper imports

## 📖 Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **React Documentation**: https://reactjs.org/docs/
- **AWS Cognito Guide**: https://docs.aws.amazon.com/cognito/
- **Docker Compose Reference**: https://docs.docker.com/compose/
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/ 