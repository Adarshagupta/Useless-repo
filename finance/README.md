# Finance App

A comprehensive finance application with real-time market data, portfolio tracking, and news.

## Features

- Real-time market data (stocks, indices)
- Portfolio management
- Financial news
- User authentication
- Dark mode UI
- Pull-to-refresh animations

## Tech Stack

### Frontend
- React Native with Expo
- TypeScript
- Axios for API requests
- Victory Charts for data visualization
- Lucide React Native for icons

### Backend
- FastAPI (Python)
- PostgreSQL
- SQLAlchemy ORM
- Alembic for migrations
- JWT authentication
- Yahoo Finance API integration

## Setup Instructions

### Prerequisites
- Node.js and npm
- Python 3.9+
- Docker and Docker Compose

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Run the setup script to create a virtual environment, install dependencies, start PostgreSQL, and initialize the database:
   ```bash
   ./setup.sh
   ```

3. Start the backend server:
   ```bash
   python run.py
   ```

   The API will be available at http://localhost:8000.

### Frontend Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the Expo development server:
   ```bash
   npm run dev
   ```

3. Use the Expo Go app on your mobile device to scan the QR code, or press 'w' to open in a web browser.

## Using the Application

### Authentication
- Use the following credentials to log in:
  - Email: user@example.com
  - Password: password

### Development Mode
- By default, the frontend uses mock data for development.
- To use the real backend, set `USE_MOCK_DATA = false` in `app/api/index.ts`.

## API Documentation

When the backend is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Running Both Frontend and Backend

You can use the start script to run both the frontend and backend:

```bash
./start.sh
```

This will:
1. Start PostgreSQL using Docker
2. Run database migrations
3. Initialize the database with sample data
4. Start the backend server
5. Start the frontend application
