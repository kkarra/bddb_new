import os
from flask import Flask
from flask.ext.mail import Message, Mail
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'development key'

app.config["MAIL_SERVER"] = "smtp.stanford.edu"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'bddb_help_me@lists.stanford.edu'
#app.config["MAIL_PASSWORD"] = 'your password'

UPLOAD_FOLDER = '/Users/curator/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'bed', 'rtf'])

app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

dbhost = 'localhost'
dbport = '3306'
dbuser = 'root'
dbpass = ''
dbname = 'broad_domains_new'
SQLALCHEMY_DATABASE_URI = 'mysql://' + dbuser + ':' + dbpass + '@' + dbhost + ':' + dbport + '/' + dbname

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

from app import views, models

if __name__ == '__main__':
    app.run(debug=True)