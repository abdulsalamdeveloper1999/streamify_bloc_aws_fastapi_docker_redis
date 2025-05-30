# Streamify

A modern streaming platform built with FastAPI, PostgreSQL, and Docker. This project provides a robust backend infrastructure for handling video streaming, authentication, and data management.

## 🚀 Features

- FastAPI-based REST API
- PostgreSQL database integration
- Docker containerization
- AWS Cognito authentication
- Video transcoding capabilities
- Message queue consumer for async processing

## 🏗️ Project Structure

```
.
├── backend/           # FastAPI backend service
├── transcoder/        # Video transcoding service
├── consumer/          # Message queue consumer
└── README.md
```

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **Authentication**: AWS Cognito
- **Containerization**: Docker
- **Message Queue**: (To be implemented)
- **Video Processing**: (To be implemented)

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.8+
- AWS Account (for Cognito)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/streamify.git
   cd streamify
   ```

2. Set up environment variables:
   Create a `.env` file in the backend directory with the following variables:
   ```
   DATABASE_URL=postgresql://postgres:test123@db:5432/mydatabase
   AWS_COGNITO_USER_POOL_ID=your_pool_id
   AWS_COGNITO_CLIENT_ID=your_client_id
   ```

3. Start the services using Docker Compose:
   ```bash
   cd backend
   docker-compose up --build
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔧 Development

### Backend Development

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```bash
   uvicorn main:app --reload
   ```

## 🐳 Docker Services

The project uses Docker Compose to manage multiple services:

- **FastAPI Backend**: Runs on port 8000
- **PostgreSQL Database**: Runs on port 5432

## 🔐 Authentication

The application uses AWS Cognito for authentication. Make sure to:
1. Set up a Cognito User Pool
2. Configure the necessary environment variables
3. Update the CORS settings in `main.py` if needed

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- FastAPI documentation
- PostgreSQL documentation
- Docker documentation 