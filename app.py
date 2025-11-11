from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta, date
from config import Config
from models import db, User, Movie, Order, Review
from forms import *
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
with app.app_context():
    db.create_all()
    if not User.query.filter_by(email='admin@booking4u.com').first():
        admin = User(
            name='Admin User',
            email='admin@booking4u.com',
            phone='1234567890',
            address='123 Admin St',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: admin@booking4u.com / admin123")

    if Movie.query.count() == 0:
        sample_movies = [
        Movie(
            title='Black Phone 2',
            synopsis='As Finn, now 17, struggles with life after his captivity, his sister begins receiving calls in her dreams from the black phone and seeing disturbing visions of three boys being stalked at a winter camp known as Alpine Lake.',
            cast='Ethan Hawke, Mason Thames, Madeleine Mcgraw, Miguel Mora, Jeremy Davies, Arianna Rivas, James Ransone, etc...',
            director='Scott Derrickson',
            runtime=114,
            genre='Horror',
            release_date=datetime(2025, 10, 17).date(),
            is_upcoming=False,
            price=12.00,
            image_url='https://m.media-amazon.com/images/M/MV5BMTVjMzNmZGYtOWU5NS00NDYzLThhZTktZGNlODIwYWVhMDRmXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg',
            trailer_url='https://www.youtube.com/watch?v=v0kqkRZHqk4'
        ),
        Movie(
            title='Predator: Badlands',
            synopsis='follows a young, exiled Predator named Dek who, after his brother is killed, is sent to a remote planet. There, he reluctantly teams up with a Weyland-Yutani synthetic named Thia (Elle Fanning) to survive and hunt the ultimate prey, which is a dangerous creature on the planet, to gain revenge against his father',
            cast='Elle Fanning, Dimitrius Koloamatangi, Mike Homik, Rohinal Nayaran',
            director='Dan Trachtenberg',
            runtime=107,
            genre='Sci-Fi/Horror',
            release_date=datetime(2025, 11, 7).date(),
            is_upcoming=False,
            price=14.00,
            image_url='https://m.media-amazon.com/images/M/MV5BNTdjZGUxMTItNjRkNS00N2VhLWE4MjMtMjVhODMwMGIxNjUwXkEyXkFqcGc@._V1_.jpg',
            trailer_url='https://www.youtube.com/watch?v=43R9l7EkJwE'
        ),
        Movie(
            title='Avatar 3',
            synopsis='Fire and Ash will follow the Sully family as they deal with the grief of losing Neteyam, while simultaneously facing a new conflict with the aggressive "Ash People" tribe, led by Varang',
            cast='Sam Worthington, Zoe Saldana, Sigourney Weaver',
            director='James Cameron',
            runtime=180,
            genre='Sci-Fi',
            release_date=datetime(2025, 12, 20).date(),
            is_upcoming=True,
            price=14.00,
            image_url='https://m.media-amazon.com/images/M/MV5BZDYxY2I1OGMtN2Y4MS00ZmU1LTgyNDAtODA0MzAyYjI0N2Y2XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg',
            trailer_url='https://www.youtube.com/watch?v=Ma1x7ikpid8'
        ),
        Movie(
            title='Now You See Me, Now You Dont',
            synopsis='The original Four Horsemen reunite with a new generation of illusionists to take on a powerful diamond heiress, Veronika Vanderberg, who leads a criminal empire built on money laundering and trafficking.',
            cast='Dave Franco, Isla Fisher, Morgan Freeman, Jesse Eisenberg, Mark Ruffalo, Daniel Radcliffe',
            director='Ruben Fleischer',
            runtime=180,
            genre='Action/Thriller',
            release_date=datetime(2025, 11, 14).date(),
            is_upcoming=True,
            price=14.00,
            image_url='https://m.media-amazon.com/images/M/MV5BYmZmZDc1Y2EtMmU2MS00NmMzLTllZmYtNjlkODFkNjZlOGE0XkEyXkFqcGc@._V1_QL75_UX190_CR0,0,190,281_.jpg',
            trailer_url='https://www.youtube.com/watch?v=-E3lMRx7HRQ'
        ),
         Movie(
            title='Frankenstein',
            synopsis='A brilliant but egotistical scientist brings a monstrous creature to life in a daring experiment that ultimately leads to the undoing of both the creator and his tragic creation.',
            cast='Jacob Elordi, Mia Goth, Oscar Isaac, Christoph Waltz, Felix Kammerer, etc...',
            director='Guillermo del Toro',
            runtime=149,
            genre='Horror/Sci-Fi',
            release_date=datetime(2025, 10, 17).date(),
            is_upcoming=False,
            price=12.00,
            image_url='https://image.tmdb.org/t/p/original/wWuB5zIdCLxpjO0tzTjwE9TTLjg.jpg',
            trailer_url='https://www.youtube.com/watch?v=x--N03NO130'
        ),
        Movie(
            title='Tron: Ares',
            synopsis='Mankind encounters AI beings for the first time when a highly sophisticated programme, Ares, leaves the digital world for a dangerous mission in the real world.',
            cast='Jared Leto, Greta Lee, Evan Peters, Cameron Monaghan, Jeff Bridges, Sarah Desjardins, etc...',
            director='Joachim Rønning',
            runtime=119,
            genre='Sci-Fi/Action',
            release_date=datetime(2025, 10, 10).date(),
            is_upcoming=False,
            price=14.00,
            image_url='https://m.media-amazon.com/images/I/610xYe0sQIL._AC_UF894,1000_QL80_.jpg',
            trailer_url='https://www.youtube.com/watch?v=YShVEXb7-ic'
        ),
        Movie(
            title='Wicked: For Good',
            synopsis='Now demonized as the Wicked Witch of the West, Elphaba lives in exile in the Ozian forest, while Glinda resides at the palace in Emerald City, reveling in the perks of fame and popularity. As an angry mob rises against the Wicked Witch, she will need to reunite with Glinda to transform herself, and all of Oz, for good.',
            cast='Ariana Grande, Cynthia Erivo, Jonathan Bailey, Jeff Goldblum, etc...',
            director='Jon M. Chu',
            runtime=137,
            genre='Musical/Fantasy',
            release_date=datetime(2025, 10, 21).date(),
            is_upcoming=True,
            price=15.00,
            image_url='https://www.movieposters.com/cdn/shop/files/wicked_for_good_1024x1024.jpg?v=1750177305',
            trailer_url='https://www.youtube.com/watch?v=R2Xubj7lazE'
        ),
        Movie(
            title='Long Shadows',
            synopsis='The story follows FBI consultant Amos Decker as he investigates the murders of a federal judge and her bodyguard in South Florida.',
            cast='Blaine Maye, Dermot Mulroney, Dominic Monaghan, Jacqueline Bisset, etc...',
            director='William Shockley',
            runtime=100,
            genre='Western',
            release_date=datetime(2025, 11, 7).date(),
            is_upcoming=False,
            price=12.00,
            image_url='https://m.media-amazon.com/images/M/MV5BOTgwMzJiODQtZDcxMy00ZWUwLTkyMTMtZjIyMjYwNzljNWNhXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg',
            trailer_url='https://www.youtube.com/watch?v=kFbOejT0XSw'
        ),
        Movie(
            title='David',
            synopsis='In a fear-ruled kingdom, a young shepard dares to face a giant and the darkness behind him. His courage awakens a nation, proving true strength comes from trust, not power.',
            cast='Phil Wickham, Brandon Engman, Lauren Daigle, Brian Stivale, etc...',
            director='Phil Cunningham, Brent Dawes',
            runtime=115,
            genre='Western',
            release_date=datetime(2025, 12, 19).date(),
            is_upcoming=True,
            price=15.00,
            image_url='https://m.media-amazon.com/images/M/MV5BNWU2ZWVmM2UtOTczZC00ZDU3LWEwZDMtZjc3YTJlOTk4MzY2XkEyXkFqcGc@._V1_.jpg',
            trailer_url='https://www.youtube.com/watch?v=cyBHli_akQw'
        ),
        Movie(
            title='Christy',
            synopsis='Christy Martin never imagined life beyond her small-town roots in West Virginia, until she discovered a knack for punching people. Fueled by grit, raw determination, and an unshakable desire to win, she charges into the world of boxing under the guidance of her trainer and manager turned husband, Jim.',
            cast='Blaine Maye, Dermot Mulroney, Dominic Monaghan, Jacqueline Bisset, etc...',
            director='David Michod',
            runtime=1135,
            genre='Sport/Drama',
            release_date=datetime(2025, 11, 7).date(),
            is_upcoming=False,
            price=12.00,
            image_url='https://m.media-amazon.com/images/M/MV5BM2E5MjhjODgtYzg0MS00NTlhLWIyZTktYjRjOTM1MDJlZWI4XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg',
            trailer_url='https://www.youtube.com/watch?v=YCuj6LpRgGM'
        ),
        ] 
        db.session.add_all(sample_movies)
        db.session.commit()
        print("Sample movies added")

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
    
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/forgot-username', methods=['GET', 'POST'])
def forgot_username():
    """Send username to user's email"""
    form = ForgotUsernameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash(f'Your username (email) is: {user.email}', 'info')
        else:
            flash('No account found with that email address.', 'danger')
        return redirect(url_for('login'))
    
    return render_template('forgot_username.html', form=form)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Password reset request"""
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Password reset instructions have been sent to your email.', 'info')
        else:
            flash('No account found with that email address.', 'danger')
        return redirect(url_for('login'))
    
    return render_template('forgot_password.html', form=form)

@app.route('/home')
@login_required
def home():
    """Main homepage after login"""
    return render_template('home.html')

@app.route('/movies/current')
@login_required
def current_movies():
    """Display current movies"""
    movies = Movie.query.filter_by(is_upcoming=False).all()
    return render_template('current_movies.html', movies=movies)

@app.route('/movies/upcoming')
@login_required
def upcoming_movies():
    """Display upcoming movies"""
    movies = Movie.query.filter_by(is_upcoming=True).all()
    return render_template('upcoming_movies.html', movies=movies)

@app.route('/movies/search', methods=['GET', 'POST'])
@login_required
def search_movies():
    """Search for movies"""
    form = MovieSearchForm()
    movies = []
    
    if form.validate_on_submit():
        search_query = form.search_query.data
        movies = Movie.query.filter(Movie.title.ilike(f'%{search_query}%')).all()
    
    return render_template('search_movies.html', form=form, movies=movies)

@app.route('/movie/<int:movie_id>')
@login_required
def movie_detail(movie_id):
    """Display movie details and reviews"""
    movie = Movie.query.get_or_404(movie_id)
    reviews = Review.query.filter_by(movie_id=movie_id).order_by(Review.created_at.desc()).all()
    review_form = ReviewForm()
    
    return render_template('movie_detail.html', movie=movie, reviews=reviews, review_form=review_form)

@app.route('/movie/<int:movie_id>/review', methods=['POST'])
@login_required
def add_review(movie_id):
    """Add a review for a movie"""
    movie = Movie.query.get_or_404(movie_id)
    form = ReviewForm()
    
    if form.validate_on_submit():
        existing_review = Review.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
        if existing_review:
            flash('You have already reviewed this movie.', 'warning')
        else:
            review = Review(
                user_id=current_user.id,
                movie_id=movie_id,
                rating=form.rating.data,
                comment=form.comment.data
            )
            db.session.add(review)
            db.session.commit()
            flash('Review submitted successfully!', 'success')
    
    return redirect(url_for('movie_detail', movie_id=movie_id))

@app.route('/book/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def book_ticket(movie_id):
    """Book tickets for a movie"""
    movie = Movie.query.get_or_404(movie_id)
    
    if movie.is_upcoming:
        flash('Cannot book tickets for upcoming movies.', 'warning')
        return redirect(url_for('movie_detail', movie_id=movie_id))
    
    form = BookTicketForm()
    form.theater.choices = [(t, t) for t in app.config['THEATERS']]
    form.showtime.choices = [(s, s) for s in app.config['SHOWTIMES']]
    
    if form.validate_on_submit():
        session['booking'] = {
            'movie_id': movie_id,
            'theater': form.theater.data,
            'showtime': form.showtime.data,
            'show_date': form.show_date.data.isoformat(),
            'num_tickets': form.num_tickets.data
        }
        return redirect(url_for('checkout'))
    
    return render_template('book_ticket.html', movie=movie, form=form)

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout and payment"""
    if 'booking' not in session:
        flash('No booking information found.', 'warning')
        return redirect(url_for('current_movies'))
    
    booking = session['booking']
    movie = Movie.query.get_or_404(booking['movie_id'])
    total_price = movie.price * booking['num_tickets']
    
    form = CheckoutForm()
    
    if form.validate_on_submit():
        order = Order(
            order_number=Order.generate_order_number(),
            user_id=current_user.id,
            movie_id=movie.id,
            theater=booking['theater'],
            showtime=booking['showtime'],
            show_date=datetime.fromisoformat(booking['show_date']).date(),
            num_tickets=booking['num_tickets'],
            total_price=total_price,
            payment_method=form.payment_method.data,
            status='unused'
        )
        
        db.session.add(order)
        db.session.commit()
        
        session.pop('booking', None)
        
        flash(f'Payment successful! Your order number is: {order.order_number}', 'success')
        return redirect(url_for('order_history'))
    
    return render_template('checkout.html', movie=movie, booking=booking, total_price=total_price, form=form)

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    form = UpdateProfileForm(obj=current_user)
    return render_template('profile.html', form=form)

@app.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    """Update user profile"""
    form = UpdateProfileForm()
    
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
    
    return redirect(url_for('profile'))


@app.route('/orders')
@login_required
def order_history():
    """View order history"""
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('order_history.html', orders=orders)

@app.route('/order/<int:order_id>/refund', methods=['POST'])
@login_required
def refund_order(order_id):
    """Request refund for an order"""
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('order_history'))
    
    if order.can_refund():
        order.status = 'refunded'
        db.session.commit()
        flash('Refund processed successfully!', 'success')
    else:
        flash('Refund not available. Orders must be cancelled at least 24 hours before showtime.', 'warning')
    
    return redirect(url_for('order_history'))

@app.route('/admin')
@login_required
def admin_panel():
    """Admin dashboard"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('home'))
    
    total_tickets = db.session.query(db.func.sum(Order.num_tickets)).filter(Order.status != 'refunded').scalar() or 0
    total_revenue = db.session.query(db.func.sum(Order.total_price)).filter(Order.status != 'refunded').scalar() or 0
    movies = Movie.query.all()

    
    return render_template('admin_panel.html', 
                          total_tickets=total_tickets, 
                          total_revenue=total_revenue,
                          movies=movies,
                          today=date.today()
                          )


@app.route('/admin/movie/add', methods=['GET', 'POST'])
@login_required
def add_movie():
    """Add new movie"""
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))
    
    form = AddMovieForm()
    
    if form.validate_on_submit():
        movie = Movie(
            title=form.title.data,
            synopsis=form.synopsis.data,
            director=form.director.data,
            cast=form.cast.data,
            runtime=form.runtime.data,
            genre=form.genre.data,
            release_date=form.release_date.data,
            is_upcoming=form.is_upcoming.data,
            price=form.price.data,
            image_url=form.image_url.data,
            trailer_url=form.trailer_url.data
        )
        db.session.add(movie)
        db.session.commit()
        
        flash('Movie added successfully!', 'success')
        return redirect(url_for('admin_panel'))
    
    return render_template('add_movie.html', form=form)


@app.route('/admin/movie/<int:movie_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_movie(movie_id):
    """Edit existing movie"""
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))
    
    movie = Movie.query.get_or_404(movie_id)
    form = EditMovieForm(obj=movie)
    
    if form.validate_on_submit():
        movie.title = form.title.data
        movie.synopsis = form.synopsis.data
        movie.director = form.director.data
        movie.cast = form.cast.data
        movie.runtime = form.runtime.data
        movie.genre = form.genre.data
        movie.release_date = form.release_date.data
        movie.is_upcoming = form.is_upcoming.data
        movie.price = form.price.data
        movie.image_url = form.image_url.data
        movie.trailer_url = form.trailer_url.data
        
        db.session.commit()
        flash('Movie updated successfully!', 'success')
        return redirect(url_for('admin_panel'))
    
    return render_template('edit_movie.html', form=form, movie=movie)


@app.route('/admin/movie/<int:movie_id>/delete', methods=['POST'])
@login_required
def delete_movie(movie_id):
    """Delete a movie"""
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))
    
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    
    flash('Movie deleted successfully!', 'success')
    return redirect(url_for('admin_panel'))


@app.route('/admin/add-admin', methods=['GET', 'POST'])
@login_required
def add_admin():
    """Grant admin access to a user"""
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))
    
    form = AddAdminForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.is_admin:
                flash('User is already an admin.', 'info')
            else:
                user.is_admin = True
                db.session.commit()
                flash(f'Admin access granted to {user.email}', 'success')
        else:
            flash('User not found.', 'danger')
        
        return redirect(url_for('admin_panel'))
    
    return render_template('add_admin.html', form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)