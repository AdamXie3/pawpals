from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_socketio import SocketIO
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')

# Database configuration
if os.environ.get('DATABASE_URL'):
    # Render PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
else:
    # Local SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pawpals.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
socketio = SocketIO(app)

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    user_type = db.Column(db.String(20))  # 'owner' or 'sitter'
    bio = db.Column(db.Text)
    location = db.Column(db.String(128))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    pets = db.relationship('Pet', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    species = db.Column(db.String(32))
    breed = db.Column(db.String(64))
    age = db.Column(db.Integer)
    description = db.Column(db.Text)
    photo_url = db.Column(db.String(256))
    status = db.Column(db.String(20))  # 'available', 'adopted', 'sitting'
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        recent_pets = Pet.query.order_by(Pet.created_at.desc()).limit(6).all()
    else:
        recent_pets = []
    return render_template('index.html', recent_pets=recent_pets)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        user_type = request.form.get('user_type')

        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))

        user = User(email=email, name=name, user_type=user_type)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        
        flash('Invalid email or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/pets')
def pets():
    pets = Pet.query.all()
    return render_template('pets.html', pets=pets)

@app.route('/map')
def map():
    users = User.query.all()
    return render_template('map.html', users=users)

@app.route('/chat/<int:user_id>')
@login_required
def chat(user_id):
    other_user = User.query.get_or_404(user_id)
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp.asc()).all()
    return render_template('chat.html', other_user=other_user, messages=messages)

@app.route('/add_pet', methods=['GET', 'POST'])
@login_required
def add_pet():
    if request.method == 'POST':
        name = request.form.get('name')
        species = request.form.get('species')
        breed = request.form.get('breed')
        age = request.form.get('age')
        description = request.form.get('description')
        status = request.form.get('status', 'available')

        pet = Pet(
            name=name,
            species=species,
            breed=breed,
            age=age,
            description=description,
            status=status,
            owner_id=current_user.id
        )
        db.session.add(pet)
        db.session.commit()
        flash('Pet added successfully!', 'success')
        return redirect(url_for('pets'))

    return render_template('add_pet.html')

# SocketIO events
@socketio.on('send_message')
def handle_message(data):
    message = Message(
        sender_id=current_user.id,
        receiver_id=data['receiver_id'],
        content=data['message']
    )
    db.session.add(message)
    db.session.commit()
    
    socketio.emit('new_message', {
        'sender_id': current_user.id,
        'content': data['message'],
        'timestamp': message.timestamp.isoformat()
    }, room=data['receiver_id'])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)
