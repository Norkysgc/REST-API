from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_planet = db.Table('user_planet',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('planet_id', db.Integer, db.ForeignKey('planets.id')))

user_people = db.Table('user_people',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('people_id', db.Integer, db.ForeignKey('people.id')))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    # Favorites
    favorite_planet = db.relationship('Planets', secondary=user_planet)
    favorite_people = db.relationship('People', secondary=user_people)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    birthyear = db.Column(db.String(50))
    homeworld = db.Column(db.String(100))

    def __repr__(self):
        return '<People %r>' % self.id

    def serialize(self):
        return {
            "Name": self.name,
            "ID": self.id,
            "Height": self.height,
            "Mass": self.mass,
            "Birthyear": self.birthyear,
            "Homeworld": self.homeworld
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    diameter = db.Column(db.Integer)
    population = db.Column(db.Integer)
    climate = db.Column(db.String(100))
    terrain = db.Column(db.String(100))

    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return {
            "Name": self.name,
            "ID": self.id,
            "Diameter": self.diameter,
            "Population": self.population,
            "Climate": self.climate,
            "Terrain": self.terrain
        }