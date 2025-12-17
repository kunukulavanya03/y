# y

Backend API for y

## Tech Stack

- **Frontend**: React
- **Backend**: FastAPI + SQLAlchemy
- **Frontend Source**: GitHub ([Repository](https://github.com/HimaShankarReddyEguturi/Hotelbookinguidesign.git))

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
- Password reset
- User profile management

## API Endpoints

- `POST /api/register` - Register a new user account
- `POST /api/login` - Log in to an existing user account
- `POST /api/password_reset` - Reset a user's password
- `GET /api/profile` - Get the current user's profile information
- `PUT /api/profile` - Update the current user's profile information
- `DELETE /api/profile` - Delete the current user's account

## License

MIT
