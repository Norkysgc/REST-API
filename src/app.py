"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == "GET":
        users = User.query.all()
        results = [user.serialize() for user in users]
        response_body = {"message": "ok",
                        "results": results,
                        "Total_records": len(results)}
        return response_body, 200
    elif request.method == "POST":
        request_body = request.get_json()
        user = User(email = request_body['email'],
                    password = request_body['password'])
        db.session.add(user)
        db.session.commit()
        response_body = {"details": request_body,
                         "message": "User created"}
        return response_body, 200
    else:
        response_body = {"message": "Error. Method not allowed."}
        return response_body, 400

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        results = user.serialize()
        response_body = {"message": "ok",
                         "total_records": 1,
                         "results": results}
        return response_body, 200
    else:
        response_body = {"message": "record not found"}
        return response_body, 200

@app.route('/people', methods=['GET', 'POST'])
def people():
    if request.method == "GET":
        peoples = People.query.all()
        results = [people.serialize() for people in peoples]
        response_body = {"message": "ok",
                        "results": results,
                        "Total_records": len(results)}
        return response_body, 200
    elif request.method == "POST":
        request_body = request.get_json()
        peoples = People(email = request_body['email'],
                         password = request_body['password'])
        db.session.add(peoples)
        db.session.commit()
        response_body = {"details": request_body,
                         "message": "User created"}
        return response_body, 200
    else:
        response_body = {"message": "Error. Method not allowed."}
        return response_body, 400

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people(people_id):
    peoples = People.query.filter_by(id=people_id).first()
    if peoples:
        results = peoples.serialize()
        response_body = {"message": "ok",
                         "total_records": 1,
                         "results": results}
        return response_body, 200
    else:
        response_body = {"message": "record not found"}
        return response_body, 200

@app.route('/planets', methods=['GET'])
def planets():
    content = Planets.query.all()
    if content:
        result = [planets.serialize() for planets in content]
        response_body = {"message": "ok",
                        "results": result,
                        "Total_records": len(result)}
        return response_body, 200
    else:
        response_body = {"message": "record not found"}
        return response_body, 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    content = Planets.query.filter_by(id = planet_id).first()
    if content:
        results = content.serialize()
        response_body = {"message": "Ok",
                         "records": 1,
                         "results": results}
        return response_body, 200

@app.route('/favorites/people', methods=['GET'])
def get_fav():
    current_user = 1
    cuser = User.query.filter_by(id=current_user).first()
    content = cuser.favorite_people
    result = [favorite.name for favorite in content]
    response_body = {"message": "ok",
                     "results": result}
    return response_body, 200

@app.route('/favorites/people/<int:people_id>', methods=['POST', 'DELETE'])
def mod_people_fav(people_id):
    if request.method == "POST":
        current_user = 1
        cuser = User.query.filter_by(id=current_user).first() # Usuario que está haciendo cosas
        fav_people = People.query.filter_by(id=people_id).first() # Personaje que vamos a añadir
        if fav_people in cuser.favorite_people:
            response_body = {"message": "Error. Already exists"}
            return response_body, 400
        else:
            cuser.favorite_people.append(fav_people)
            db.session.commit()
            response_body = {"message": "ok",
                            "added": fav_people.name}
            return response_body, 200
    elif request.method == "DELETE":
        current_user = 1
        cuser = User.query.filter_by(id=current_user).first() # Usuario que está haciendo cosas
        fav_people = People.query.filter_by(id=people_id).first() # Personaje que vamos a eliminar
        if fav_people in cuser.favorite_people:
            cuser.favorite_people.remove(fav_people)
            db.session.commit()
            response_body = {"message": "ok",
                            "deleted": fav_people.name}
            return response_body, 200
        else:
            response_body = {"message": "Error. Record not found."}
            return response_body, 404
    else:
        response_body = {"message": "Error. Method not allowed."}
        return response_body, 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)