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


#用户退出登录
@users.route('/logout')
def logout_views():
    del session['id']
    del session['loginname']
    return redirect('/')


#用户注册功能
@users.route('/register',methods=['POST','GET'])
def register_views():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        loginname = request.form['loginname']
        uname = request.form['uname']
        email = request.form['email']
        url = request.form.get('url',None)
        upwd = request.form['password']
        print(locals())
        user = User.query.filter_by(loginname=loginname).first()
        if user:
            return "用户名已存在"
        return "注册成功"


#注册界面判断用户名是否可用
@users.route('/checkUname')
def check_uname():
    loginname = request.args['loginname']
    user = User.query.filter_by(loginname=loginname).first()
    if user:
        return '0'
    else:
        return '1'