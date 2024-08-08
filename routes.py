from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User, Sponsor, Influencer, Campaign, Ad_Request
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
  if username == "" or password == "":
    flash('Username or password cannot be empty.')
    return redirect(url_for('login_post'))
  user = User.query.filter_by(username=username).first()
  if not user:
    flash('User does not exist.')
    return redirect(url_for('login'))
  if not user.check_password(password):
    flash('Incorrect password.')
    return redirect(url_for('login'))
  # if the login is succesful
  return redirect(url_for('index'))

@app.route('/register/admin')
def register_admin():
  return render_template('register-admin.html')

@app.route('/register/admin', methods=['POST'])
def register_admin_post():
  username = request.form.get('username')
  password = request.form.get('password')
  if username == "" or password == "":
    flash('Username or password cannot be empty.')
    return redirect(url_for('register_admin'))
  user = User.query.filter_by(username=username).first()
  if user:
    flash('Username already exists. Please select some other username.')
    return redirect(url_for('register_admin'))
  user = User(username = username, password = password, type = 'admin')
  db.session.add(user)
  db.session.commit()
  flash('User successfully registered.')
  return redirect(url_for('login'))

@app.route('/register/sponsor')
def register_sponsor():
  return render_template('register-sponsor.html')

@app.route('/register/sponsor', methods=['POST'])
def register_sponsor_post():
  username = request.form.get('username')
  password = request.form.get('password')
  name = request.form.get('name')
  industry = request.form.get('industry')
  budget = request.form.get('budget')
  if username == "" or password == "":
    flash('Username or password cannot be empty.')
    return redirect(url_for('register_sponsor'))
  try:
    float(budget)
  except ValueError:
    flash('Budget must be a number.')
    return redirect(url_for('register_sponsor'))
  user = User.query.filter_by(username=username).first()
  if user:
    flash('Username already exists. Please select some other username.')
    return redirect(url_for('register_sponsor'))
  new_user = User(username = username, password = password, type = 'sponsor')
  db.session.add(new_user)
  user = User.query.filter_by(username=username).first()
  sponsor = Sponsor(user_id = user.id, name = name, industry = industry, budget = budget)
  db.session.add(sponsor)
  db.session.commit()
  flash('User successfully registered.')
  return redirect(url_for('login'))

@app.route('/register/influencer')
def register_influencer():
  return render_template('register-influencer.html')

@app.route('/register/influencer', methods=['POST'])
def register_influencer_post():
  username = request.form.get('username')
  password = request.form.get('password')
  category = request.form.get('category')
  name = request.form.get('name')
  niche = request.form.get('niche')
  reach = request.form.get('reach')
  try:
    int(reach)
  except ValueError:
    flash('Reach must be an integer.')
    return redirect(url_for('register_influencer'))
  if username == "" or password == "":
    flash('Username or password cannot be empty.')
    return redirect(url_for('register_influencer'))
  user = User.query.filter_by(username=username).first()
  if user:
    flash('Username already exists. Please select some other username.')
    return redirect(url_for('register_influencer'))
  new_user = User(username = username, password = password, type = 'influencer')
  db.session.add(new_user)
  user = User.query.filter_by(username=username).first()
  influencer = Influencer(user_id = user.id, name = name, category = category, niche = niche, reach = reach)
  db.session.add(influencer)
  db.session.commit()
  flash('User successfully registered.')
  return redirect(url_for('login'))