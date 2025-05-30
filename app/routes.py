from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import  login_user, logout_user, current_user, login_required
from sqlalchemy import text
import sqlalchemy as sa
from app.models import User
from urllib.parse import urlsplit
from werkzeug.security import generate_password_hash



@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Reg'}
    posts =[
        {
            'author':{'username':'John'},
            'body':'Portland 的天氣真好'
        },
        {
            'author':{'username': 'Susan'},
            'body': '復仇者聯盟電影真的很酷！'
        }
    ]
    return render_template('index.html', title='首頁', user=user, posts=posts)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('無效的使用者名稱或密碼')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='登入', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)

        sql = text("""
            INSERT INTO user (username, email, password_hash)
            VALUES (:username, :email, :password_hash)
        """)

        db.session.execute(sql, {
            'username': form.username.data,
            'email': form.email.data,
            'password_hash': hashed_password
        })
        db.session.commit()

        flash('恭喜，你現在是一名註冊使用者！')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': '測試貼文 #1'},
        {'author': user, 'body': '測試貼文 #2'}
    ]
    return render_template('user.html', user=user, posts=posts)
