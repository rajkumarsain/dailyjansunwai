from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import os
import uuid
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    #return render_template('index.html')  # This should display text in the browser
    return "<h1>Hello, this is raw HTML returned directly from Flask.</h1>"
if __name__ == '__main__':
    app.run(debug=True)

    app = Flask(__name__)
