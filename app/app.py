from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
import secrets
import logging

# Constants
size_choices = [('', 'Pick a size'),
    ("2XS", "2XS"),
    ("XS", "XS"),
    ("S", "S"),
    ("M", "M"),
    ("L", "L"),
    ("XL", "XL"),
    ("2XL", "2XL"),
    ("3XL", "3XL"),
    ("4XL", "4XL"),
    ("5XL", "5XL"),
    ("6XL", "6XL"),
    ("7XL", "7XL"),
    ("8XL", "8XL"),
    ('not_req', 'Not required')]

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
csrf = CSRFProtect(app)

# Define Blueprint
form_bp = Blueprint('form', __name__, template_folder='templates')

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers

# Form class
class GearRequestForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired()], render_kw={'placeholder': 'John'})
    lastName = StringField('Last Name', validators=[DataRequired()], render_kw={'placeholder': 'Smith'})
    longSleeveGreenShirt = SelectField('Long Sleeve Green Shirt', choices=size_choices)
    tShirt = SelectField('T-Shirt', choices=size_choices)
    jacket = SelectField('Jacket', choices=size_choices)
    rainJacket = SelectField('Rain Jacket', choices=size_choices)
    rainPants = SelectField('Rain Pats', choices=size_choices)
    submit = SubmitField('Submit')

# Route in Blueprint
@form_bp.route('/', methods=['GET', 'POST'])
def home():
    form = GearRequestForm()
    message = None
    if request.method == 'POST':
        if form.validate_on_submit():
            flash('Form submitted successfully!', 'success')

            # Redirect to result route with name and color as query parameters
            return redirect(url_for('form.result', firstName=form.firstName.data))
    return render_template('index.html', form=form)

# Route for displaying result (GET)
@form_bp.route('/result')
def result():
    firstName = request.args.get('firstName', '')
    message = f"Hello {firstName}, form submitted successfully!"
    return render_template('result.html', message=message)

# Error handler for CSRF errors
@app.errorhandler(400)
def bad_request(e):
    if 'CSRF' in str(e):
        flash('CSRF token is missing or invalid. Please try again.', 'error')
        return redirect(url_for('form.home'))
    return render_template('error.html', error=str(e)), 400

# Register Blueprint
app.register_blueprint(form_bp)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
else:
    app.run(debug=True)
