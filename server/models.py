# server/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

# Naming convention for migrations
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

# --------------------------
# Models
# --------------------------
class Zookeeper(db.Model, SerializerMixin):
    __tablename__ = "zookeepers"
    serialize_rules = ('-animals.zookeeper',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    birthday = db.Column(db.Date, nullable=False)

    animals = db.relationship('Animal', back_populates='zookeeper')

    def __repr__(self):
        return f"<Zookeeper {self.id}: {self.name}>"

class Enclosure(db.Model, SerializerMixin):
    __tablename__ = "enclosures"
    serialize_rules = ('-animals.enclosure',)

    id = db.Column(db.Integer, primary_key=True)
    environment = db.Column(db.String, nullable=False)
    open_to_visitors = db.Column(db.Boolean, default=True)

    animals = db.relationship('Animal', back_populates='enclosure')

    def __repr__(self):
        return f"<Enclosure {self.id}: {self.environment}>"

class Animal(db.Model, SerializerMixin):
    __tablename__ = "animals"
    serialize_rules = ('-zookeeper.animals', '-enclosure.animals',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    species = db.Column(db.String, nullable=False)

    zookeeper_id = db.Column(db.Integer, db.ForeignKey('zookeepers.id'))
    enclosure_id = db.Column(db.Integer, db.ForeignKey('enclosures.id'))

    zookeeper = db.relationship('Zookeeper', back_populates='animals')
    enclosure = db.relationship('Enclosure', back_populates='animals')

    def __repr__(self):
        return f"<Animal {self.id}: {self.name}, {self.species}>"
