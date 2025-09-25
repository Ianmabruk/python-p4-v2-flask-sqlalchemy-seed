# server/seed.py

from faker import Faker
from random import choice as rc, randint
from app import app
from models import db, Zookeeper, Enclosure, Animal

with app.app_context():
    fake = Faker()

    # Clear existing data
    Animal.query.delete()
    Zookeeper.query.delete()
    Enclosure.query.delete()

    # Create Zookeepers
    zookeepers = [Zookeeper(name=fake.name(), birthday=fake.date_of_birth(minimum_age=25, maximum_age=65)) for _ in range(3)]
    db.session.add_all(zookeepers)
    db.session.commit()

    # Create Enclosures
    environments = ['Savannah', 'Jungle', 'Ocean', 'Desert', 'Mountain']
    enclosures = [Enclosure(environment=rc(environments), open_to_visitors=rc([True, False])) for _ in range(5)]
    db.session.add_all(enclosures)
    db.session.commit()

    # Create Animals
    species_list = ['Elephant', 'Tiger', 'Bear', 'Monkey', 'Snake']
    animals = []
    for _ in range(10):
        animal = Animal(
            name=fake.first_name(),
            species=rc(species_list),
            zookeeper_id=rc(zookeepers).id,
            enclosure_id=rc(enclosures).id
        )
        animals.append(animal)
    db.session.add_all(animals)
    db.session.commit()

    print(f"Seeded {len(zookeepers)} zookeepers, {len(enclosures)} enclosures, and {len(animals)} animals.")
