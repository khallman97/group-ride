# Group Fitness App

A social fitness app for runners and cyclists to find and create group rides/runs.

## 🎯 Purpose

Build a simple, local-first app that helps runners and cyclists find and create group rides/runs. The app is NOT a fitness tracker — it is a social connector. The app focuses on simplicity, privacy, and community.

## 🚀 Features

### ✅ Completed Features
- **User Authentication** - AWS Cognito integration with email verification
- **User Profiles** - Complete profile management with preferences
- **Onboarding Flow** - 3-step guided setup for new users
- **Sports Preferences** - Running, cycling, pace, distance, availability
- **Responsive Design** - Mobile-first, works on web, iOS, Android

### 🚧 Coming Soon
- **Event Management** - Create and browse fitness events
- **Event Discovery** - Find nearby events based on preferences
- **Chat System** - Event-specific messaging
- **Maps Integration** - Location-based features
- **Notifications** - Event reminders and updates

## 🏗️ Project Structure

```
group-fitness-app/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py            # Main FastAPI application
│   │   ├── config.py          # Environment configuration
│   │   ├── database.py        # Database connection
│   │   ├── models/            # SQLAlchemy models
│   │   │   └── user.py        # User profile & preferences
│   │   ├── routers/           # API endpoints
│   │   │   ├── auth.py        # Authentication routes
│   │   │   └── users.py       # User management routes
│   │   ├── schemas/           # Pydantic schemas
│   │   │   ├── auth.py        # Auth request/response models
│   │   │   └── user.py        # User profile models
│   │   ├── services/          # Business logic
│   │   │   ├── auth_service.py    # AWS Cognito integration
│   │   │   └── user_service.py    # User management
│   │   └── utils/             # Utilities
│   │       └── auth_dependencies.py  # Auth middleware
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Backend container
│   └── create_tables.py      # Database initialization
├── frontend/                  # React Native Web frontend
│   ├── src/
│   │   ├── components/        # Reusable components
│   │   │   ├── auth/          # Authentication forms
│   │   │   └── onboarding/    # Onboarding flow
│   │   ├── contexts/          # React contexts
│   │   │   └── AuthContext.tsx  # Authentication state
│   │   ├── services/          # API communication
│   │   │   └── api.ts         # FastAPI client
│   │   ├── App.tsx           # Main application
│   │   └── index.tsx         # Entry point
│   ├── package.json          # Node dependencies
│   └── Dockerfile           # Frontend container
├── infra/                    # Infrastructure configs
├── designs/                  # UI/UX designs
├── docker-compose.yml        # Local development setup
├── env.example              # Environment template
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- AWS Account (for Cognito setup)
- Node.js 18+ (for local development)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd group-fitness-app
```

### 2. Configure Environment
```bash
# Copy environment template
cp env.example .env

# Edit .env with your AWS Cognito credentials
# AWS_REGION=us-east-1
# COGNITO_USER_POOL_ID=us-east-1_xxxxxxxxx
# COGNITO_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Start Services
```bash
# Start all services (backend, frontend, database, etc.)
docker-compose up -d

# Create database tables
docker-compose exec backend python create_tables.py
```

### 4. Access Applications
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001 (minioadmin/minioadmin)

## 🔧 Development

### Backend (FastAPI)
```bash
# View logs
docker-compose logs backend

# Access backend container
docker-compose exec backend bash

# Run tests (when implemented)
docker-compose exec backend pytest
```

### Frontend (React Native Web)
```bash
# View logs
docker-compose logs frontend

# Install new dependencies
docker-compose exec frontend npm install <package>

# Access frontend container
docker-compose exec frontend sh
```

### Database
```bash
# Access PostgreSQL
docker-compose exec postgres psql -U dev_user -d group_fitness_dev

# View database data
docker-compose exec postgres psql -U dev_user -d group_fitness_dev -c "SELECT * FROM user_profiles;"
```

## 🏗️ Architecture

### Tech Stack
- **Backend**: FastAPI (Python) with PostgreSQL
- **Frontend**: React Native Web with TypeScript
- **Authentication**: AWS Cognito
- **Storage**: S3 (production) / MinIO (local)
- **Caching**: Redis
- **Deployment**: Docker + Docker Compose

### Key Design Principles
- **Local-First**: Everything runs locally for development
- **Mobile-First**: Responsive design for all screen sizes
- **API-First**: Clean separation between frontend and backend
- **Type-Safe**: TypeScript throughout the frontend
- **Documented**: Comprehensive API documentation with FastAPI

## 🔐 Authentication Flow

1. **Sign Up** → User creates account with email/password
2. **Email Confirmation** → User enters 6-digit code from email
3. **Sign In** → User logs in with confirmed credentials
4. **Profile Creation** → System creates basic profile
5. **Onboarding** → User completes preferences (3 steps)
6. **Main App** → User can access all features

## 🗄️ Database Schema

### User Profiles
```sql
user_profiles (
  id, user_id, email, name, bio,
  location_lat, location_lng, location_name,
  created_at, updated_at
)
```

### User Preferences
```sql
user_preferences (
  id, user_id, sports[], preferred_pace,
  ride_type, distance_range_min, distance_range_max,
  availability[], created_at, updated_at
)
```

## 🚀 Deployment

### Local Development
Already configured with Docker Compose - just run `docker-compose up -d`

### Production (AWS)
- **API**: ECS/Fargate or EC2
- **Database**: RDS PostgreSQL
- **Storage**: S3
- **Authentication**: Cognito
- **Frontend**: S3 + CloudFront or Vercel

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests (when test suite is implemented)
5. Submit a pull request

## 📝 API Documentation

Visit http://localhost:8000/docs when running locally to see the interactive API documentation.

### Key Endpoints
- `POST /auth/signup` - Create new user account
- `POST /auth/signin` - User login
- `GET /auth/me` - Get current user info
- `GET /users/profile` - Get user profile
- `PUT /users/preferences` - Update user preferences
- `POST /users/onboarding` - Complete onboarding

## 🐛 Troubleshooting

### Common Issues

**Frontend not loading:**
```bash
docker-compose logs frontend
docker-compose restart frontend
```

**Backend authentication errors:**
```bash
# Check environment variables
docker-compose exec backend python -c "from app.config import get_settings; print(get_settings().__dict__)"
```

**Database connection issues:**
```bash
# Check database status
docker-compose exec postgres pg_isready
```

## 📄 License

[Add your license here]

## 🙋 Support

For questions or issues, please [create an issue](link-to-issues) in this repository. 