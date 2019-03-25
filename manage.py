'''
Created on 2017415

@author: zhou
'''

import os
from app import create_app, db
from app.models import User, Role, Comment, Post, Permission, Follow
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from flask import request, current_app


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
# migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Comment=Comment, Post=Post, Permission=Permission, Follow=Follow)


manager.add_command("shell", Shell(make_context=make_shell_context))
# manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(use_debugger=True, host='0.0.0.0', port='9980'))


@manager.command
def deploy():
    from flask_migrate import upgrade
    from app.models import Role, User, Post, Permission
    # db.drop_all()
    # db.create_all()
    upgrade()
    Role.insert_roles()
    # User.add_self_follows()
    # p = Post.query.all()
    # print p
    # page = request.args.get('page',1, type=int)
    # pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page,
    # per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
    # print pagination


@manager.command
def clearAlembic():
    from flask_migrate import upgrade
    from app.models import Alembic
    Alembic.clear_A()


if __name__ == '__main__':
    manager.run(default_command='runserver')

