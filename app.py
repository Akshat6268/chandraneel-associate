from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
# Enable CORS so the frontend HTML files can communicate with the backend
CORS(app)

# Configure the SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///c:/Users/Akshat/OneDrive/Desktop/Vs Code file/HTML File/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model for User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

# Create the database tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Collect properties
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    
    # Validation
    if not full_name or not email or not password:
        return jsonify({"success": False, "message": "All fields are required"}), 400
        
    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"success": False, "message": "User with this email already exists"}), 409
        
    # Hash password and create user
    hashed_pass = generate_password_hash(password)
    new_user = User(full_name=full_name, email=email, password_hash=hashed_pass)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"success": True, "message": "Registration successful"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "An error occurred during registration"}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required"}), 400
        
    user = User.query.filter_by(email=email).first()
    
    if user and check_password_hash(user.password_hash, password):
        # Login is successful
        return jsonify({
            "success": True, 
            "message": "Login successful",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email
            }
        })
    else:
        # Invalid credentials
        return jsonify({"success": False, "message": "Invalid email or password"}), 401

@app.route('/api/submit_inquiry', methods=['POST'])
def submit_inquiry():
    data = request.get_json()
    # Log inquiry data (simple print for now, can add to DB/file later)
    print("New inquiry received:", data)
    return jsonify({"success": True, "message": "Inquiry submitted successfully. Our team will contact you soon."})

if __name__ == '__main__':
    # Running on localhost port 5000 as requested by frontend
    app.run(debug=True, host='0.0.0.0', port=5000)
