#与博客相关的路由和视图
import datetime
import os

from . import main
from flask import render_template, request, session,redirect
from ..models import *
from .. import db


@main.route('/')
def main_index():
    #查询category中的所有分类信息
    categories = Category.query.all()
    #查询出Topic中的前20条数据
    topics = Topic.query.limit(20).all()
    if 'id' in session and 'loginname' in session:
        #已经登录过，从数据库获取登录信息
        id = session['id']
        user = User.query.filter_by(ID=id).first()
    return render_template('index.html',params=locals())


@main.route('/release',methods=['GET','POST'])
def release_views():
    if request.method == 'GET':
        url = request.headers.get('Referer','/')
        #权限验证，判断是否有用户登录以及登陆者的身份是否为作者，如果无权限，会原地址
        if 'id' in session and 'loginname' in session:
            id = session['id']
            user = User.query.filter_by(ID=id).first()
            #判断是否有发布博客的权限
            if user.is_author == 1:
                # 查询category的信息
                categories = Category.query.all()
                return render_template('release.html', params=locals())
            else:
                return redirect(url)
        else:
            return redirect('/login')
    else:
        #post请求，用户发表博客
        topic = Topic()
        topic.title = request.form['title']
        topic.blogtype_id = request.form['blogtype_id']
        topic.category_id = request.form['category']
        topic.content = request.form['content']
        topic.user_id = session['id']
        topic.pub_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #判断是否有文件上传,如果有则将文件保存值static/upload,并将路径存入topic.images
        if request.files:
            #获取上传文件
            f = request.files['image']
            # 处理文件名：时间.扩展名
            ftime = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            ext = f.filename.split('.')[-1]
            filename = ftime + '.' + ext
            #上传文件：/static/upload/xxx.xxx  先找到上一个路径>>>>>>>>>>>>>>>>>>>>>>>>>>>
            basedir = os.path.dirname(os.path.dirname(__file__))
            upload_path = os.path.join(basedir,'static/upload', filename)
            f.save(upload_path)
            #文件路径赋值给topic.images
            topic.images = 'upload/' + filename
        db.session.add(topic)
        return redirect('/')


@main.route('/info')
def info_views():
    basedir = os.path.dirname(__file__)
    print(basedir)
    return render_template('info.html')
