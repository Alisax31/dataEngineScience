from flask import Flask
from flask import Blueprint
from flask import request as req
from flask import session
from flask import redirect
from flask import url_for
from flask import flash
from flask import render_template
#app = Flask(__name__)

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/login', methods=('GET','POST'))
def login():
    if req.method == 'POST':
        error = None
        username = req.form['username']
        pwd = req.form['pwd']
        if username is None:
            error = "用户名为空"
        if pwd is None:
            error = "密码为空"
        print(type(username))
        print(type(pwd))
        if  username == 'admin' and pwd == 'admin' and error is None:
            session.clear()
            session['username']=username
            return redirect(url_for('index'))
        else:
            error = "用户名密码错误"           
        flash(error)
    return render_template('user/loginNew.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user.login'))