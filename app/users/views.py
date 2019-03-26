#处理与用户业务相关的视图和路由
from . import users
from flask import redirect,render_template,request,session
from ..models import *
from .. import db
import datetime


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
        user = User()
        user.loginname = request.form['loginname']
        user.uname = request.form['uname']
        user.email = request.form['email']
        user.upwd = request.form['upwd']
        url = request.form.get('url')
        if url:
            user.url = url
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print('err=',e)
            return "注册失败，请联系管理员"
        session['loginname'] = request.form['loginname']
        session['id'] = user.ID
        return redirect('/')


#注册界面判断用户名是否可用
@users.route('/checkUname')
def check_uname():
    loginname = request.args['loginname']
    user = User.query.filter_by(loginname=loginname).first()
    if user:
        return '0'
    else:
        return '1'


@users.route('/reply',methods=['POST'])
def reply_views():
    if request.method == 'POST':
        url = request.headers['Referer']
        print(url)
        user_id = session['id']
        topic_id = request.form['topic_id']
        content = request.form['reply']
        reply_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        reply = Reply()
        reply.user_id = user_id
        reply.topic_id = topic_id
        reply.content = content
        reply.reply_time = reply_time
        print(locals())
        try:
            db.session.add(reply)
            db.session.commit()
        except Exception as err:
            print('留言板块插入异常:',err)
        return redirect(url)
