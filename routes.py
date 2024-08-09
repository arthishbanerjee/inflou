from functools import wraps
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Sponsor, Influencer, Campaign, Ad_Request
from app import app

def auth_required(func):
  @wraps(func)
  def inner(*args, **kwargs):
    if 'user_id' not in session:
      flash('Please log in to continue.')
      return redirect(url_for('login'))
    return func(*args, **kwargs)
  return inner

def admin_required(func):
  @wraps(func)
  def inner(*args, **kwargs):
    if 'user_id' in session:
      user = User.query.get(session['user_id'])
      if user.type != 'admin':
        flash('You must be an admin to access this page.')
        return redirect(url_for('logout'))
    else:
      flash('You need to login first.')
      return redirect(url_for('login'))
    return func(*args, **kwargs)
  return inner

def sponsor_required(func):
  @wraps(func)
  def inner(*args, **kwargs):
    if 'user_id' in session:
      user = User.query.get(session['user_id'])
      if user.type != 'sponsor':
        flash('You must be a sponsor to access this page.')
        return redirect(url_for('logout'))
    else:
      flash('You need to login first.')
      return redirect(url_for('login'))
    return func(*args, **kwargs)
  return inner

def influencer_required(func):
  @wraps(func)
  def inner(*args, **kwargs):
    if 'user_id' in session:
      user = User.query.get(session['user_id'])
      if user.type != 'influencer':
        flash('You must be an influencer to access this page.')
        return redirect(url_for('logout'))
    else:
      flash('You need to login first.')
      return redirect(url_for('login'))
    return func(*args, **kwargs)
  return inner

@app.route('/')
def index():
  # return render_template('index.html', user = User.query.get(session['user_id']))
  return redirect(url_for('login'))

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
@admin_required
def admin_home():
  user = User.query.filter_by(id=session['user_id']).first()
  return render_template('home-admin.html', user=user)

@app.route('/sponsor/home')
@sponsor_required
def sponsor_home():
  user = User.query.filter_by(id=session['user_id']).first()
  sponsor = Sponsor.query.filter_by(user_id=session['user_id']).first()
  if not user:
    flash('Improper access. You have been logged out.')
    return redirect(url_for('logout'))
  return render_template('home-sponsor.html', sponsor=sponsor, user=user)

@app.route('/sponsor/campaigns')
@sponsor_required
def sponsor_campaigns():
  user = User.query.filter_by(id=session['user_id']).first()
  sponsor = Sponsor.query.filter_by(user_id=session['user_id']).first()
  campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id)
  return render_template('campaigns-sponsor.html', sponsor=sponsor, user=user, campaigns=campaigns)

@app.route('/sponsor/campaigns/<int:id>/delete')
@sponsor_required
def sponsor_campaigns_delete(id):
  campaign = Campaign.query.filter_by(id=id).first()
  if not campaign:
    flash('Campaign does not exist.')
    return redirect(url_for('sponsor_campaigns'))
  db.session.delete(campaign)
  db.session.commit()
  return redirect(url_for('sponsor_campaigns'))

@app.route('/sponsor/campaigns', methods=['POST'])
@sponsor_required
def sponsor_campaigns_post():
  sponsor = Sponsor.query.filter_by(user_id=session['user_id']).first()
  description = request.form.get('description')
  start_date = request.form.get('start_date')
  end_date = request.form.get('end_date')
  budget = request.form.get('budget')
  visibility = request.form.get('visibility')
  goal = request.form.get('goal')
  start_dt = datetime.strptime(start_date, '%Y-%m-%d')
  end_dt = datetime.strptime(end_date, '%Y-%m-%d')
  if end_dt < start_dt:
    flash('End date cannot be before the start date.')
    return redirect(url_for('sponsor_campaigns'))
  try:
    float(budget)
  except ValueError:
    flash('Budget must be a number.')
    return redirect(url_for('sponsor_campaigns'))
  try:
    int(goal)
  except ValueError:
    flash('Goal must be an integer.')
    return redirect(url_for('sponsor_campaigns'))
  campaign = Campaign(sponsor_id=sponsor.id, description=description, start_date=start_dt, end_date=end_dt, budget=budget, visibility=visibility, goal=goal)
  db.session.add(campaign)
  db.session.commit()
  return redirect(url_for('sponsor_campaigns'))

@app.route('/influencer/home')
@influencer_required
def influencer_home():
  user = User.query.filter_by(id=session['user_id']).first()
  influencer = Influencer.query.filter_by(user_id=session['user_id']).first()
  if not influencer:
    flash('Improper access. You have been logged out.')
    return redirect(url_for('logout'))
  return render_template('home-influencer.html', influencer=influencer, user=user)

@app.route('/influencer/find')
@influencer_required
def influencer_find():
  user = Influencer.query.filter_by(user_id=session['user_id']).first()
  if not user:
    flash('Improper access. You have been logged out.')
    return redirect(url_for('logout'))
  return render_template('home-influencer.html', user=user)

@app.route('/influencer/stats')
@influencer_required
def influencer_stats():
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