from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    # add relationship
    pizzas = relationship('Pizza', secondary='restaurant_pizzas', back_populates='restaurants')

    # add serialization rules

    serialize_rules = ('-restaurant_pizzas.restaurant',)

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
    pizzas = relationship('Pizza', secondary='restaurant_pizzas', back_populates='restaurants')
    # add serialization rules
    serialize_rules = ('-restaurant_pizzas.pizza',)

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # add relationships

    restaurant_id = db.Column(db.Integer, ForeignKey('restaurants.id', ondelete='CASCADE'), nullable=False)
    restaurant = relationship('Restaurant', backref=backref('restaurant_pizzas', cascade='all, delete-orphan'))

    pizza_id = db.Column(db.Integer, ForeignKey('pizzas.id', ondelete='CASCADE'), nullable=False)
    pizza = relationship('Pizza', backref=backref('restaurant_pizzas', cascade='all, delete-orphan'))


    # add serialization rules
    serialize_rules = ('-restaurant',)

    # add validation

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"