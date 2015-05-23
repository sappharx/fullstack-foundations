from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/', methods = ['GET'])
@app.route('/restaurants/', methods = ['GET'])
def showRestaurants():
	if request.method == 'GET':
		restaurants = session.query(Restaurant).all()
		return render_template('restaurants.html', restaurants = restaurants)
	
@app.route('/restaurant/new', methods = ['GET', 'POST'])
def newRestaurant():
	if request.method == 'GET':
		return render_template('newRestaurant.html')
	elif request.method == 'POST':
		newRestaurant = Restaurant(name = request.form['name'])
		session.add(newRestaurant)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id = newRestaurant.id))
	
@app.route('/restaurant/<int:restaurant_id>/edit', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'GET':
		return render_template('editRestaurant.html', restaurant = restaurant)
	elif request.method == 'POST':
		if request.form['name']:
			restaurant.name = request.form['name']
		session.add(restaurant)
		session.commit()
		#items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
		return redirect(url_for('showMenu', restaurant_id = restaurant.id))#, items = items))
	
@app.route('/restaurant/<int:restaurant_id>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'GET':
		return render_template('deleteRestaurant.html', restaurant = restaurant)
	elif request.method == 'POST':
		session.delete(restaurant)
		session.commit()
		#restaurants = session.query(Restaurant).all()
		return redirect(url_for('showRestaurants'))#, restaurants = restaurants))
	
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id, methods = ['GET']):
	if request.method == 'GET':
		restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
		items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
		return render_template('menu.html', restaurant = restaurant, items = items)
	
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'GET':
		restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
		return render_template('newMenuItem.html', restaurant = restaurant)
	elif request.method == 'POST':
		newItem = MenuItem(name = request.form['name'],
						   course = request.form['course'],
						   price = request.form['price'],
						   description = request.form['description'],
						   restaurant_id = restaurant_id)
		
		session.add(newItem)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	item = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'GET':
		return render_template('editMenuItem.html', restaurant = restaurant, item = item)
	elif request.method == 'POST':
		
		if request.form['name']:
			item.name = request.form['name']
		if request.form['course']:
			item.course = request.form['course']
		if request.form['price']:
			item.price = request.form['price']
		if request.form['description']:
			item.description = request.form['description']

		session.add(item)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))
	
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	item = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'GET':
		return render_template('deleteMenuItem.html', restaurant = restaurant, item = item)
	elif request.method == 'POST':
		session.delete(item)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id = restaurant_id))


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)