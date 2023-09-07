from flask import Flask, render_template, request, redirect
from database import db_session, init_db
from models.restaurants import Restaurants
import datetime

app = Flask(__name__)


@app.before_first_request
def init():
    init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def start():
    return 'Hello World!'


@app.route('/create-restaurant', methods=['GET', 'POST'])
def create_restaurant():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        site_url = request.form.get('site_url')

        restaurant = Restaurants(name=name, description=description, site_url=site_url)
        db_session.add(restaurant)
        db_session.commit()

        return '{}, {}, {}'.format(name, description, site_url)

    return render_template('create_restaurant.html')


@app.route('/restaurants')
def restaurant_list():
    restaurants = Restaurants.query.all()

    return render_template('restaurant.html', restaurants=restaurants)


@app.route('/edit-restaurant', methods=['GET', 'POST'])
def edit_restaurant():
    id = request.args.get('id')

    restaurant = Restaurants.query.filter(Restaurants.id == id).first()

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        site_url = request.form.get('site_url')

        restaurant.name = name
        restaurant.description = description
        restaurant.site_url = site_url
        restaurant.modified_time = datetime.datetime.now()

        db_session.commit()

        return redirect('/restaurants')

    return render_template('edit_restaurant.html', restaurant=restaurant)


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(debug=True)
