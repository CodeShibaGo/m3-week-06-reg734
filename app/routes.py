from flask import render_template
from app import app

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