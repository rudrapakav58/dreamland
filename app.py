from flask import Flask, render_template, request, redirect, session, flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "thIsisaSecret!"

@app.route('/', methods = ['GET','POST'])
def index():
    res=request.form.to_dict()
    #print res
    return render_template('landingpage.html')
@app.route('/reg', methods = ['GET','POST'])
def newuser():

    return render_template('index.html')
@app.route('/create', methods=['POST'])
def create():
    #print "In create"
    error = False
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    password_confirmation = request.form['password_confirmation']
    #print request.form

    if len(first_name) < 1:
        error = True
        flash('First name cannot be blank')

    if first_name.isalpha():
        flash('First name is usable')
    else:
        flash("Please enter a valid First name")

    if last_name.isalpha():
        flash('Last name is usable')
    else:
        flash("Please enter a valid Last name")

    if len(last_name) < 1:
        error = True
        flash('Last name cannot be blank')

    if len(email) < 3:
        error = True
        flash('Email cannot be blank')
    if len(password) < 8:
        error = True
        flash('Please enter a valid Password')
    if len(password_confirmation) < 8:
        error = True
        flash('Please enter password confirmation')
    if not EMAIL_REGEX.match(email):
        error = True
        flash('Email is invalid')
    if password != password_confirmation:
        error = True
        flash('Passwords do not match')

    if error is True:
        return redirect('/')

    flash('You Are Now A Registered User!')
    return redirect('/')
app.run(debug=True,port=5005)