#处理与用户业务相关的视图和路由
from . import users
from flask import redirect,render_template,request,session
from ..models import *
from .. import db


@users.route('/login',methods=['GET','POST'])
def login_views():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        loginname = request.form['username']
        upwd = request.form['password']
        user = User.query.filter_by(loginname=loginname,upwd=upwd).first()
        if user:
            #将id和loginname同时存进session
            session['loginname'] = loginname
            session['id'] = user.ID
            return redirect('/')
        else:
            return redirect('/login')