# PawPals

PawPals is a community-driven pet care platform that connects pet owners with potential adopters and pet sitters. The platform facilitates pet adoption, pet sitting services, and community building among pet lovers.

## Features

- **User Profiles**
  - Custom profiles for pet owners and pet sitters/adopters
  - Profile customization and updates
  - Pet information management

- **Pet Management**
  - Upload pet information and photos
  - Manage adoption listings
  - Pet sitting availability calendar

- **Community Features**
  - Built-in real-time chat system
  - Interactive community map
  - Pet owner and sitter reviews

- **Search & Discovery**
  - Find pets for adoption
  - Locate pet sitters in your area
  - Search by pet type, location, and availability

## Installation

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

6. Run the application:
```bash
flask run
```

## Technologies Used

- Flask (Python web framework)
- SQLAlchemy (Database ORM)
- Flask-SocketIO (Real-time chat)
- Google Maps API (Community mapping)
- Flask-Login (User authentication)
- SQLite/PostgreSQL (Database)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
