from os import name, urandom
from flask import Flask, jsonify, request, render_template, redirect, url_for, session
import flask
from flask.helpers import flash
from api.user.users import user, Userlogin
from api.database.database import DataCrude
from flask_login import login_user, logout_user, login_required, LoginManager
app = Flask(__name__)
base = DataCrude()
login_manager = LoginManager(app)
app.config['SECRET_KEY'] = base.seckeyget()
