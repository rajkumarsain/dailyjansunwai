from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import os
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'dlo.doit.alwar@gmail.com'
app.config['MAIL_PASSWORD'] = 'Analaysis@123'
app.config['MAIL_DEFAULT_SENDER'] = 'dlo.doit.alwar@gmail.com'

mail = Mail(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from models import User, Question, Reply


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Send verification email function
def send_verification_email(user):
    token = str(uuid.uuid4())  # Generate a unique token
    user.verification_token = token
    db.session.commit()

    msg = Message('Email Verification - CleanAlwar', recipients=[user.email])
    verification_link = url_for('verify_email', token=token, _external=True)
    msg.body = f"Please click the following link to verify your email: {verification_link}"
    mail.send(msg)


# User registration with email verification
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']  # role: 'admin' or 'client'
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash('Email already exists.')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_password, role=role, verified=False)
            db.session.add(new_user)
            db.session.commit()

            send_verification_email(new_user)
            flash('Registration successful! Please check your email to verify your account.')
            return redirect(url_for('login'))

    return render_template('register.html')


# Email verification route
@app.route('/verify/<token>')
def verify_email(token):
    user = User.query.filter_by(verification_token=token).first()
    if user:
        user.verified = True
        user.verification_token = None
        db.session.commit()
        flash('Email verified successfully! You can now login.')
        return redirect(url_for('login'))
    else:
        flash('Invalid or expired token.')
        return redirect(url_for('register'))


# User login with verification check and password hashing
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            if user.verified:
                login_user(user)
                if user.role == 'admin':
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('client'))
            else:
                flash('Please verify your email before logging in.')
        else:
            flash('Login failed. Check your email or password.')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Admin and client routes (same as before)
# ...


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
