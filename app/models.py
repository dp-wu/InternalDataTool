import datetime
from email.policy import default

from pytz import utc
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager


# 提前定义多对多关系表
# 标签与推荐记录的关联表，附加置信度字段
classification = db.Table(
    'classification',
    db.Column('recommendation_id', db.Integer, db.ForeignKey('recommendation.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('confidence', db.Float, default=0.0, comment='机器学习模型预测的置信度')  # 置信度字段
)

# 定义核心数据模型
class SysUser(UserMixin, db.Model):
    """
    系统用户模型，包含认证信息和用户角色
    用户包括admin，employee等不同角色
    通过Flask-Login进行用户会话管理
    """
    __tablename__ = 'sys_user' # 指定数据库表名,以防和其它类型的user表冲突
    id = db.Column(db.Integer, primary_key=True)

    # 登陆凭证
    username = db.Column(db.String(64), unique=True, nullable=False, indexable=True, comment='用户名')
    email = db.Column(db.String(120), unique=True, nullable=False, comment='用户邮箱')
    password_hash = db.Column(db.String(128), nullable=False, comment='密码哈希值')
    role = db.Column(db.String(20), default='system_user', comment='用户角色：admin或user')

    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(utc), comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(utc), onupdate=datetime.datetime.now(utc), comment='最后更新时间')

    # 关系：该系统用户的查询历史
    query_history = db.relationship('QueryHistory', backref='user', lazy='dynamic')

    # 密码安全方法
    def set_password(self, password):
        """设置用户密码，存储哈希值"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证用户密码"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<SysUser {self.username}>'


class DoubanUser(db.Model):
    """
    豆瓣用户模型，存储豆瓣用户的基本信息
    """
    __tablename__ = 'douban_user'
    id = db.Column(db.Integer, primary_key=True)

    douban_id = db.Column(db.String(64), unique=True, nullable=False, index=True, comment='豆瓣用户ID')
    name = db.Column(db.String(120), nullable=False, comment='豆瓣用户名')
    profile_url = db.Column(db.String(255), comment='豆瓣用户主页URL')

    # 关系：该豆瓣用户的推荐记录
    recommendations = db.relationship('Recommendation', backref='douban_user', lazy='dynamic',cascade='all, delete-orphan', single_parent=True)

    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(utc), comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(utc), onupdate=datetime.datetime.now(utc), comment='最后更新时间')


    def __repr__(self):
        return f'<DoubanUser {self.name} ({self.douban_id})>'


class Book(db.Model):
    """
    书籍：我们最关心的核心实体，所有推荐都围绕书籍展开。
    以豆瓣图书ID (douban_id) 作为唯一标识。
    """
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)

    douban_book_id = db.Column(db.String(64), unique=True, nullable=False, index=True, comment='豆瓣书籍ID')
    title = db.Column(db.String(255), nullable=False, comment='书名')
    author = db.Column(db.String(255), comment='作者')
    publisher = db.Column(db.String(255), comment='出版社')
    url = db.Column(db.String(255), comment='豆瓣书籍URL')
    cover_image = db.Column(db.String(255), comment='封面图片URL')

    # 关系：该书籍的推荐记录
    recommendations = db.relationship('Recommendation', backref='book', lazy='dynamic',cascade='all, delete-orphan', single_parent=True)

    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(utc), comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(utc), onupdate=datetime.datetime.now(utc), comment='最后更新时间')


    def __repr__(self):
        return f'<Book {self.title} ({self.douban_book_id})>'


class Recommendation(db.Model):
    """
    推荐记录模型，存储每次推荐的结果
    关联豆瓣用户和书籍，并包含推荐时间和标签
    """
    __tablename__ = 'recommendation'
    id = db.Column(db.Integer, primary_key=True)

    # 核心内容：友邻写的推荐语，笔记等
    summary = db.Column(db.Text, comment='推荐摘要或说明')
    recommended_at = db.Column(db.DateTime, index=True, comment='推荐时间（豆瓣广播时间')
    crawled_at = db.Column(db.DateTime, default=datetime.datetime.now(utc), comment='数据抓取时间')
    source_url = db.Column(db.String(255), unique=True, nullable=False, comment='推荐来源URL，用于去重')

    # 外键关联：谁推荐的，推荐的哪本书
    douban_user_id = db.Column(db.Integer, db.ForeignKey('douban_user.id'), nullable=False, comment='关联的豆瓣用户ID')
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False, comment='关联的书籍ID')

    # 多对多关系：推荐标签及其置信度
    tags = db.relationship('Tag', secondary=classification,
                           backref=db.backref('recommendations', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return f'<Recommendation {self.id} by User{self.douban_user_id} for Book{self.book_id}>'


class Tag(db.Model):
    """
    标签模型，存储推荐标签，提前定义好用于机器学习分类
    通过多对多关系与推荐记录关联
    """
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64), unique=True, nullable=False, comment='标签名称，如“游记”、“科幻”等')
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(utc), comment='创建时间')

    def __repr__(self):
        return f'<Tag {self.name}>'


# Flask-Login 要求：提供根据ID加载系统用户对象的函数
@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login 在每次请求时调用此函数来加载用户
    """
    # 注意：这里的 id 是字符串，需要转换为整数
    return SysUser.query.get(int(user_id))