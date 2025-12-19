# y

Backend API for y

## Tech Stack

- **Frontend**: React
- **Backend**: FastAPI + SQLAlchemy
- **Frontend Source**: GitHub ([Repository](https://github.com/HimaShankarReddyEguturi/Hotelbookinguidesign))

## Project Structure

```
y/
├── frontend/          # Frontend application
├── backend/           # Backend API
├── README.md          # This file
└── docker-compose.yml # Docker configuration (if applicable)
```

## Getting Started

### Prerequisites

- Node.js 18+ (for frontend)
- Python 3.11+ (for Python backends)
- Docker (optional, for containerized setup)

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Backend Setup

```bash
cd backend
# Follow backend-specific setup instructions in backend/README.md
```

## Features

- User registration
- User login
- User profile management
- Password reset
- User listing

## API Endpoints

- `POST /api/register` - Create a new user account
- `POST /api/login` - Authenticate a user
- `GET /api/profile` - Retrieve the current user's profile information
- `PUT /api/profile` - Update the current user's profile information
- `POST /api/password-reset` - Reset the current user's password
- `GET /api/users` - Retrieve a list of all users

## License

MIT
