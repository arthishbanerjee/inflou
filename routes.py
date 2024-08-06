from flask import Flask, render_template, request, redirect, url_for, flash
import models
from app import app

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/register/admin')
def register_admin():
  return render_template('register-admin.html')

@app.route('/register/sponsor')
def register_sponsor():
  return render_template('register-sponsor.html')

@app.route('/register/influencer')
def influencer():
  return render_template('register-influencer.html')