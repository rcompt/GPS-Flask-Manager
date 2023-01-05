# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 17:25:01 2022

@author: Stang
"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from gps_server import app
from models import db

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()