from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
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
    form = LoginForm()
    if form.validate_on_submit():
        flash('使用者{} 的登入請求, 記住我={}'.format(
            form.username.data, form.remember_me.data))
        return  redirect(url_for('index'))
    return render_template('login.html', title='登入', form=form)