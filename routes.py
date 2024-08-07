from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from models import User
from app import app

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
  username = request.form.get('username')
  password = request.form.get('password')
  user = User.query.filter_by(username=username).first()
  if not user:
    flash('User does not exist.')
    return redirect(url_for('login'))
  if not user.check_password(password):
    flash('Incorrect password.')
    return redirect(url_for('login'))
  # if the login is succesful
  return(redirect)

@app.route('/register/admin')
def register_admin():
  return render_template('register-admin.html')

@app.route('/register/sponsor')
def register_sponsor():
  return render_template('register-sponsor.html')

@app.route('/register/influencer')
def influencer():
  return render_template('register-influencer.html')