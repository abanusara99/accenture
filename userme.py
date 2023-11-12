from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Update to the correct path if needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    email = db.Column(db.String(30), primary_key=True)
    password_hash = db.Column(db.String(128))
    # If you intended to have a confirmation attribute, specify its type and other details
    # For example, assuming it's a boolean:
    confirmation = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

# Use app.app_context() to create the application context
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Error creating database tables: {e}")

# Endpoint to render the registration form
# Endpoint to render the registration form
@app.route('/register', methods=['GET'])
def registration_form():
    print("Accessed /register route")  # Add this line
    return render_template('ring.html')

# Endpoint to register a new user
@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    # Basic client-side validation
    if not email or not password or not confirm_password:
        return 'All fields are required', 400

    if password != confirm_password:
        return 'Password and Confirm Password must match', 400

    # Check if the email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return 'Email already exists', 400

    new_user = User(email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return 'Registration successful', 201

if __name__ == '__main__':
    app.run(debug=True)
