from flask import session
from flask_sqlalchemy import SQLAlchemy
from app import app
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)

## models

class User(db.Model):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key = True, nullable = False)
  username = db.Column(db.String(32), unique=True, nullable = False)
  passhash = db.Column(db.String(512), nullable = False)
  type = db.Column(db.String(16), nullable = False)

  @property
  def password(self):
    raise AttributeError('Password is not a readable attribute.')
  
  @password.setter
  def password(self, password):
    self.passhash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.passhash, password)

class Sponsor(db.Model):
  __tablename__ = 'sponsor'
  id = db.Column(db.Integer, primary_key = True, nullable = False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
  name = db.Column(db.String(64), nullable = False)
  industry = db.Column(db.String(32), nullable = False)
  budget = db.Column(db.Float, nullable = False)
  flag = db.Column(db.Boolean, default=False, nullable=False)
  # id(FK), name, industry, budget

class Influencer(db.Model):
  __tablename__ = 'influencer'
  id = db.Column(db.Integer, primary_key = True, nullable = False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
  name = db.Column(db.String(64), nullable = False)
  category = db.Column(db.String(32), nullable = False)
  niche = db.Column(db.String(32), nullable = False)
  reach = db.Column(db.Integer, nullable = False)
  earnings = db.Column(db.Float, default=0.0, nullable = False)
  flag = db.Column(db.Boolean, default=False, nullable=False)
  # id(FK), name, category, niche, reach

class Campaign(db.Model):
  __tablename__ = 'campaign'
  id = db.Column(db.Integer, primary_key = True, nullable = False)
  sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable = False)
  description = db.Column(db.String(512), nullable = False)
  start_date = db.Column(db.Date, nullable = False)
  end_date = db.Column(db.Date, nullable = False)
  budget = db.Column(db.Float, nullable = False)
  visibility = db.Column(db.Integer, nullable = False)
  goal = db.Column(db.Integer, nullable = False)
  niche = db.Column(db.String(32), default='', nullable = False)
  flag = db.Column(db.Boolean, default=False, nullable=False)
  # name, description, start_date, end_date, budget, visibility, goals

  # relationship
  ads = db.relationship('Ad_Request', backref='campaign')

class Ad_Request(db.Model):
  __tablename__ = 'ad_request'
  id = db.Column(db.Integer, primary_key = True, nullable = False)
  campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable = False)
  influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable = False)
  messages = db.Column(db.String(256), nullable = False)
  requirements = db.Column(db.String(256), nullable = False)
  payment_amount = db.Column(db.Float, nullable = False)
  sponsor_status = db.Column(db.String(16), default='pending', nullable = False)
  influencer_status = db.Column(db.String(16), default='pending', nullable = False)
  by_sponsor = db.Column(db.Boolean, default=False, nullable=False)
  by_influencer = db.Column(db.Boolean, default=False, nullable=False)
  flag = db.Column(db.Boolean, default=False, nullable=False)
  # campaign_id(FK), influencer_id, messaes, requirements, payment_amount, status

# create a database if it doesn't exist
with app.app_context():
  db.create_all()
  # create a basic admin
  admin = User.query.filter_by(username='admin').first()
  if not admin:
    admin = User(username = 'admin', password = 'admin', type = 'admin')
    db.session.add(admin)
    db.session.commit()