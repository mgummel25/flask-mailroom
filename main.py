import os

from flask import Flask, render_template, request, redirect, url_for, session
from model import Donation, Donor, User
from passlib.hash import pbkdf2_sha256
from peewee import DoesNotExist

app = Flask(__name__)
app.secret_key = b'\x02x\xa0c\xef\xd5\x08g\xab\xd9\xe5\xf9\x99\xf2\xd3\x15\xe9G\xda\xd8*\x0fL\r'

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            user = User.select().where(User.name == request.form['name']).get()
        except DoesNotExist :
            user = None

        if user and pbkdf2_sha256.verify(request.form['password'], user.password):
            session['username'] = request.form['name']
            return redirect(url_for('add_donation'))

        return render_template('login.jinja2', error="Incorrect username or password.")

    return render_template('login.jinja2')



@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/add/', methods=['GET', 'POST'])
def add_donation():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        try:
            amount = int(request.form['donation'])
            donor = Donor.select().where(Donor.name==request.form['donor']).get()
            Donation(donor=donor, value=amount).save()
            return redirect(url_for('home'))

        except IndexError:
            return render_template('add_donation.jinja2', error="Invalid Donor. Please try again!")

        except ValueError:
            return  render_template('add_donation.jinja2', error="Invalid Donation amount. Please try again!")

    return render_template('add_donation.jinja2')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port, threaded=True)

