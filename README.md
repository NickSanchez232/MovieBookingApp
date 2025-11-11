# Booking4U - Movie Ticket Booking System

A comprehensive web-based movie ticket booking system built with Flask that allows users to browse movies, book tickets, write reviews, and manage their orders.

## Features

### User Features
- **User Authentication**
  - Registration and login system
  - Password recovery
  - Profile management
  
- **Movie Browsing**
  - View current movies and upcoming releases
  - Search movies by title
  - Detailed movie information with trailers
  - Movie reviews and ratings

- **Ticket Booking**
  - Select theater location (6 locations available)
  - Choose showtime and date
  - Book multiple tickets (up to 10 per order)
  - Multiple payment methods (Credit Card, PayPal, Venmo)

- **Order Management**
  - View order history
  - Request refunds (24 hours before showtime)
  - Track order status

### Admin Features
- **Movie Management**
  - Add new movies
  - Edit existing movies
  - Delete movies
  - Manage movie details (cast, synopsis, trailers, pricing)

- **User Management**
  - Grant admin privileges to users

- **Dashboard**
  - View total tickets sold
  - Track revenue
  - Monitor all movies in the system

## Technology Stack

- **Backend**: Flask 3.0.0
- **Database**: SQLAlchemy with SQLite
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF with WTForms
- **Frontend**: Bootstrap 5.3.0
- **Password Security**: Werkzeug

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd booking4u
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser and navigate to `http://localhost:5000`

## Default Admin Account

The application creates a default admin account on first run:
- **Email**: admin@booking4u.com
- **Password**: admin123

**⚠️ Important**: Change the admin password after first login in a production environment.

## Project Structure

```
booking4u/
├── app.py                  # Main application file
├── config.py              # Configuration settings
├── models.py              # Database models
├── forms.py               # WTForms definitions
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── home.html
│   ├── current_movies.html
│   ├── upcoming_movies.html
│   ├── movie_detail.html
│   ├── search_movies.html
│   ├── book_ticket.html
│   ├── checkout.html
│   ├── order_history.html
│   ├── profile.html
│   ├── admin_panel.html
│   ├── add_movie.html
│   ├── edit_movie.html
│   ├── add_admin.html
│   ├── forgot_username.html
│   └── forgot_password.html
└── static/               # Static files (CSS, JS, images)
    ├── css/
    └── js/
```

## Database Models

### User
- Name, email, phone, address
- Password (hashed)
- Admin privileges flag
- Relationships: orders, reviews

### Movie
- Title, synopsis, cast, director
- Runtime, genre, release date
- Pricing information
- Image and trailer URLs
- Status (current/upcoming)
- Relationships: orders, reviews

### Order
- Order number (unique identifier)
- User and movie references
- Theater location, showtime, show date
- Number of tickets, total price
- Payment method
- Order status (unused/refunded)

### Review
- User and movie references
- Rating (1-5 stars)
- Comment text
- Timestamp

## Configuration

Edit `config.py` to customize:

- **SECRET_KEY**: Application secret key (change in production)
- **DATABASE_URI**: Database connection string
- **THEATERS**: Available theater locations
- **SHOWTIMES**: Available movie showtimes
- **PAYMENT_METHODS**: Accepted payment methods
- **MAX_TICKETS_PER_ORDER**: Maximum tickets per booking

## Available Theaters

- Lubbock
- Amarillo
- Levelland
- Plainview
- Snyder
- Abilene

## Available Showtimes

- 2:00 PM
- 5:00 PM
- 8:00 PM
- 10:00 PM

## Business Rules

1. **Booking Restrictions**
   - Only current movies can be booked (not upcoming releases)
   - Maximum 10 tickets per order
   - Must select future show dates

2. **Refund Policy**
   - Refunds available up to 24 hours before showtime
   - Only unused tickets can be refunded
   - Status changes from "unused" to "refunded"

3. **Reviews**
   - Users can only review each movie once
   - Ratings range from 1 to 5 stars
   - Comments are optional

## Sample Movies

The application comes pre-loaded with 10 sample movies including:
- Black Phone 2
- Predator: Badlands
- Avatar 3
- Frankenstein
- Tron: Ares
- And more...

## Security Features

- Password hashing using Werkzeug
- CSRF protection on all forms
- User session management
- Admin-only route protection
- Input validation on all forms

## Development

### Running in Debug Mode

The application runs in debug mode by default for development:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

**⚠️ Important**: Disable debug mode in production.

### Adding New Movies

Admins can add movies through the admin panel with the following information:
- Title, genre, director, cast
- Synopsis and runtime
- Release date and pricing
- Image URL (poster)
- Trailer URL (YouTube)
- Status (current/upcoming)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is created for educational purposes.

## Support

For issues or questions, please create an issue in the repository.

## Acknowledgments

- Bootstrap for responsive UI components
- Flask community for excellent documentation
- SQLAlchemy for database management

---

**Note**: This is a demonstration application. For production use, implement additional security measures, proper email functionality, payment gateway integration, and environment-specific configurations.
