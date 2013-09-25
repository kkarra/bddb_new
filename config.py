import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'


SQLALCHEMY_DATABASE_URI = 'mysql:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

dbhost = 'localhost'
dbport = '3306'
dbuser = 'root'
dbpass = ''
dbname = 'broad_domains_new'
DB_URI = 'mysql://' + dbuser + ':' + dbpass + '@' + dbhost + ':' + dbport + '/' + dbname
