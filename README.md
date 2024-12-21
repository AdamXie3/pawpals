# PawPals - Community Pet Adoption Platform

PawPals is a community-driven platform that connects pet owners with potential adopters and pet sitters. The platform features user profiles, real-time chat, a community map, and comprehensive pet management capabilities.

## Features

- **User Profiles**: Create and manage profiles for pet owners and sitters
- **Pet Management**: List pets for adoption or sitting services
- **Real-time Chat**: Built-in messaging system for users
- **Community Map**: Locate pet owners and sitters in your area
- **Modern UI**: Beautiful, responsive design using Tailwind CSS

## Tech Stack

- **Backend**: Flask, SQLAlchemy, Flask-SocketIO
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Database**: PostgreSQL (Production), SQLite (Development)
- **Authentication**: Flask-Login
- **Real-time**: Socket.IO
- **Maps**: Google Maps API

## Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pawpals.git
   cd pawpals
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Initialize the database:
   ```bash
   flask db upgrade
   ```

6. Run the development server:
   ```bash
   flask run
   ```

## Deployment to Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the following:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment Variables**:
     - `FLASK_APP`: app.py
     - `FLASK_ENV`: production
     - `SECRET_KEY`: [your-secret-key]
     - `DATABASE_URL`: [your-postgresql-url]
     - `GOOGLE_MAPS_API_KEY`: [your-api-key]

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
