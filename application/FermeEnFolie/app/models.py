from enum import Enum
from app import db, app
import json

# Définissez une énumération pour les types d'animaux
class AnimalType(Enum):
    Vachette = "Vachette"
    Cochon = "Cochon"
    Souris = "Souris"
    Ane = "Ane"
    Coq = "Coq"
    Furet = "Furet"
    Fermier = "Fermier"


class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    type = db.Column(
        db.Enum(AnimalType), nullable=False
    )  # Utilisation de l'énumération
    age = db.Column(db.Integer)
    portions = db.Column(db.Integer)

    def __repr__(self):
        return f"<Animal {self.name} ({self.type.value}), Age: {self.age}>"

    def get_type_name(self):
        return self.type.value

with app.app_context():
    db.create_all()
