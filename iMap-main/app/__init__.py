import logging
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):

    app = Flask(__name__, template_folder='templates')

    # 设置日志
    app.logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)

    # 加载配置
    app.config.from_object(config_class)

    # 创建数据库连接
    db.init_app(app)
    migrate.init_app(app, db)

    # 注册蓝图
    from app.blueprints.map import bp_map
    from app.blueprints.metro import bp_metro
    app.register_blueprint(bp_map)
    app.register_blueprint(bp_metro)

    return app
