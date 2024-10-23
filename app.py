# # app.py

# from flask import Flask, render_template, request, redirect, url_for, session, flash
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
# import requests
# from models import User, Thumbnail
# from database import db

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thumbnails.db'
# app.config['SECRET_KEY'] = 'harrypotter'  # Change this to a strong secret key
# db.init_app(app)

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# @app.before_request
# def create_tables():
#     if not hasattr(app, 'tables_created'):
#         db.create_all()
#         app.tables_created = True

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/dashboard')
# @login_required
# def dashboard():
#     user_thumbnails = Thumbnail.query.filter_by(user_id=current_user.id).all()
#     return render_template('dashboard.html', thumbnails=user_thumbnails)

# @app.route('/download_thumbnail', methods=['POST'])
# @login_required
# def download_thumbnail():
#     youtube_url = request.form['youtube_url']
#     video_id = youtube_url.split('v=')[-1] if 'v=' in youtube_url else youtube_url.split('/')[-1]

#     thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
#     thumbnail_response = requests.get(thumbnail_url)

#     if thumbnail_response.status_code == 200:
#         new_thumbnail = Thumbnail(url=thumbnail_url, user_id=current_user.id)
#         db.session.add(new_thumbnail)
#         db.session.commit()
#         return redirect(url_for('dashboard'))
#     else:
#         flash("Thumbnail not available.", "danger")
#         return redirect(url_for('dashboard'))

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         new_user = User(username=username, password=password)
#         db.session.add(new_user)
#         db.session.commit()
#         flash("Signup successful! Please log in.", "success")
#         return redirect(url_for('login'))
#     return render_template('signup.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username, password=password).first()
#         if user:
#             login_user(user)
#             return redirect(url_for('dashboard'))
#         flash("Invalid credentials. Please try again.", "danger")
#     return render_template('login.html')

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from models import User, Thumbnail
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thumbnails.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a strong secret key
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def create_tables():
    if not hasattr(app, 'tables_created'):
        db.create_all()
        app.tables_created = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user_thumbnails = Thumbnail.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', thumbnails=user_thumbnails)

@app.route('/download_thumbnail', methods=['POST'])
@login_required
def download_thumbnail():
    youtube_url = request.form['youtube_url']
    video_id = youtube_url.split('v=')[-1] if 'v=' in youtube_url else youtube_url.split('/')[-1]

    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    thumbnail_response = requests.get(thumbnail_url)

    if thumbnail_response.status_code == 200:
        new_thumbnail = Thumbnail(url=thumbnail_url, user_id=current_user.id)
        db.session.add(new_thumbnail)
        db.session.commit()
        flash("Thumbnail downloaded successfully!", "success")
        return redirect(url_for('dashboard'))
    else:
        flash("Thumbnail not available.", "danger")
        return redirect(url_for('dashboard'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])  # Hash the password
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Signup successful! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):  # Check hashed password
            login_user(user)
            return redirect(url_for('dashboard'))
        flash("Invalid credentials. Please try again.", "danger")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']
        current_user.username = username
        if new_password:
            current_user.password = generate_password_hash(new_password)
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('dashboard'))
    return render_template('profile.html', user=current_user)

if __name__ == '__main__':
    app.run(debug=True)
