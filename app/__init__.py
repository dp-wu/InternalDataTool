import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from celery import Celery
from config import Config # 导入自定义的config模块，在上级菜单里


# 创建扩展对象
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL) # 这里deepseek没传入对象，等下问问为啥pycharm推荐这么写

def create_app(config_class=Config):
    """
    创建Flask应用工厂函数
    这是flask应用的创建中心，负责初始化应用和扩展
    所有的配置，扩展初始化，和蓝图注册都在这里完成
    """

    # 创建Flask应用实例
    app = Flask(__name__)

    # 加载配置（包括数据库URI，密钥等）
    app.config.from_object(config_class)

    # 初始化celery，绑定flask应用上下文，注意这里的celery是上文的全局对象
    celery.conf.update(app.config)

    # 初始化其它扩展，绑定flask应用实例
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # 配置登录管理器
    login_manager.login_view = 'auth.login'  # 设置登录视图的端点
    login_manager.login_message = 'Please log in to access this page.'  # 设置登录提示消息
    login_manager.login_message_category = 'info'  # 设置登录消息的类别

    # 注册蓝图，将不同模块的路由组织起来（先创建蓝图对象，再注册）
    #