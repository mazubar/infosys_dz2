from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from peewee_model.my_model import *
from bokeh.plotting import figure
from bokeh.models import (FactorRange, Range1d)
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from bokeh.transform import factor_cmap
from bokeh.palettes import Spectral6

app = Flask(__name__)

@app.route('/')

def home():
	if not session.get('logged_in'):
		return render_template('login.html', title = 'Logging in')
	else:
		return render_template('homepage.html', title = 'Welcome!')


@app.route('/login', methods = ['POST'])

def do_a_login():

	def get_pass(login):
		users = User.get(User.login == login)
		return users.password

	if request.form['password'] in get_pass(request.form['username']):
		session['logged_in'] = True
	else:
		flash('wrong password!')
	return home()


@app.route('/chart')

def create_chart():	

	movies = Netflix.select().where(Netflix.type_ == "Movie")
	movies = movies.count()

	shows = Netflix.select().where(Netflix.type_ == "TV Show")
	shows = shows.count()

	names = ['Movie', 'TV Show']
	numbers = [movies, shows]

	data=dict(names=names, numbers=numbers)

	source = ColumnDataSource(data=data)

	xdr = FactorRange(factors=names)
	ydr = Range1d(start=0,end=max(numbers)*1.5)

	p = figure(x_range=names, plot_height=500, title="Movies and TV shows on Netflix", toolbar_location=None)

	p.vbar(x='names', top='numbers', source=source, width=0.9, legend='names',
       line_color='white', fill_color=factor_cmap('names', palette=Spectral6, factors=names))

	script, div = components(p)

	return render_template('chart1.html', the_div=div, the_script=script)

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(debug = True)