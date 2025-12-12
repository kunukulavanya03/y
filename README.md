# y

Backend API for y

## Tech Stack

- **Frontend**: React
- **Backend**: FastAPI + SQLAlchemy
- **Frontend Source**: GitHub ([Repository](https://github.com/HimaShankarReddyEguturi/Designpythonworldclockui.git))

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
- Data CRUD operations

## API Endpoints

- `POST /api/register` - Register a new user account.
- `POST /api/login` - Log in to an existing user account.
- `POST /api/reset-password` - Reset the password for a user account.
- `GET /api/profile` - Get the profile information for the current user.
- `PUT /api/profile` - Update the profile information for the current user.
- `POST /api/data` - Create a new data item.
- `GET /api/data` - Get a list of all data items.
- `GET /api/data/{data_id}` - Get a single data item by ID.
- `PUT /api/data/{data_id}` - Update a single data item by ID.
- `DELETE /api/data/{data_id}` - Delete a single data item by ID.

## License

MIT
