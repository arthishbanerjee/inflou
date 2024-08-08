from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Sponsor, Influencer, Campaign, Ad_Request
from app import app

def auth_required(func):
  @wraps(func)
  def inner(*args, **kwargs):
    if 'user_id' not in session:
      flash('You need to login first.')
      return redirect(url_for('login'))
    return func(*args, **kwargs)
  return inner

@app.route('/')
@auth_required
def index():
  return render_template('index.html', user = User.query.get(session['user_id']))

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
  session['user_id'] = user.id
  if user.type == 'sponsor':
    return redirect(url_for('sponsor_home'))
  if user.type == 'influencer':
    return redirect(url_for('influencer_home'))
  return redirect(url_for('admin_home'))

@app.route('/admin/home')
@auth_required
def admin_home():
  user = User.query.filter_by(id=session['user_id']).first()
  if not user.type=='admin':
    flash('Improper access. You have been logged out.')
    return redirect(url_for('logout'))
  return render_template('home-admin.html', user=user)

@app.route('/sponsor/home')
@auth_required
def sponsor_home():
  user = Sponsor.query.filter_by(user_id=session['user_id']).first()
  if not user:
    flash('Improper access. You have been logged out.')
    return redirect(url_for('logout'))
  return render_template('home-sponsor.html', user=user)

@app.route('/influencer/home')
@auth_required
def influencer_home():
  user = Influencer.query.filter_by(user_id=session['user_id']).first()
  if not user:
    flash('Improper access. You have been logged out.')
    return redirect(url_for('logout'))
  return render_template('home-influencer.html', user=user)


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

@app.route('/logout')
def logout():
  session.pop('user_id', None)
  return redirect(url_for('login'))