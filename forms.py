from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, FloatField, DateField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange
from models import User

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    address = StringField('Home Address', validators=[DataRequired(), Length(max=200)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email or login.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ForgotUsernameForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Username')


class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class UpdateProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    address = StringField('Home Address', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Update Profile')


class MovieSearchForm(FlaskForm):
    search_query = StringField('Search Movies', validators=[DataRequired()])
    submit = SubmitField('Search')


class BookTicketForm(FlaskForm):
    theater = SelectField('Theater', validators=[DataRequired()])
    showtime = SelectField('Showtime', validators=[DataRequired()])
    show_date = DateField('Show Date', validators=[DataRequired()])
    num_tickets = IntegerField('Number of Tickets', validators=[DataRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField('Proceed to Checkout')


class CheckoutForm(FlaskForm):
    payment_method = SelectField('Payment Method', choices=[
        ('credit', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('venmo', 'Venmo')
    ], validators=[DataRequired()])
    submit = SubmitField('Complete Purchase')


class ReviewForm(FlaskForm):
    rating = IntegerField('Rating (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField('Review', validators=[Length(max=500)])
    submit = SubmitField('Submit Review')


class AddMovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired(), Length(max=200)])
    genre = StringField('Genre', validators=[Length(max=100)])
    director = StringField('Director', validators=[DataRequired(), Length(max=200)])
    cast = TextAreaField('Cast', validators=[Length(max=500)])
    synopsis = TextAreaField('Synopsis')
    runtime = IntegerField('Runtime (minutes)', validators=[DataRequired()])
    price = FloatField('Ticket Price', validators=[DataRequired()])
    release_date = DateField('Release Date', validators=[DataRequired()])
    image_url = StringField('Image URL', validators=[Length(max=300)])
    trailer_url = StringField('Trailer URL', validators=[Length(max=300)])
    is_upcoming = BooleanField('Upcoming Movie')
    submit = SubmitField('Add Movie')



class EditMovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired(), Length(max=200)])
    genre = StringField('Genre', validators=[Length(max=100)])
    director = StringField('Director', validators=[DataRequired(), Length(max=200)])
    cast = TextAreaField('Cast', validators=[Length(max=500)])
    synopsis = TextAreaField('Synopsis')
    runtime = IntegerField('Runtime (minutes)', validators=[DataRequired()])
    price = FloatField('Ticket Price', validators=[DataRequired()])
    release_date = DateField('Release Date', validators=[DataRequired()])
    image_url = StringField('Image URL', validators=[Length(max=300)])
    trailer_url = StringField('Trailer URL', validators=[Length(max=300)])
    is_upcoming = BooleanField('Upcoming Movie')
    submit = SubmitField('Update Movie')


class AddAdminForm(FlaskForm):
    email = StringField('User Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Grant Admin Access')