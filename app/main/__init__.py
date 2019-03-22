#main:处理与博客相关的业务逻辑(主业务)
#如：发表/查看/删除/修改 博客...
#将自己添加到蓝图中
from flask import Blueprint
main = Blueprint("main",__name__)  #第一个参数为当前包的名称
from . import views