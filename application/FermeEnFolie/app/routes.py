from app import app, db
from flask import render_template, request, redirect, url_for
from sqlalchemy.exc import IntegrityError  # Importez l'exception d'intégrité SQLAlchemy
from app.models import Animal, AnimalType
from app.constants import *
from app.feedfarmhub import *
import random


@app.after_request
def access_logs(response):
    http_path = request.path  # Ajout du chemin HTTP demandé
    if http_path != "/metrics":
    # Récupérer des informations sur la requête
        user_agent = request.headers.get("User-Agent")
        client_ip = request.remote_addr
        http_method = request.method
        http_status = response.status_code
        # Créer un dictionnaire d'informations supplémentaires
        extra_data = {
            "http_method": http_method,
            "http_path": http_path,
            "http_status": http_status,
            "client_ip": client_ip,
            "user_agent": user_agent,
        }

        app.logger.info(msg="", extra=extra_data)
    return response


@app.route("/")
def list_animals():
    page = request.args.get(
        "page", 1, type=int
    )  # Récupère le numéro de la page depuis l'URL (par défaut : page 1)
    per_page = 10  # Nombre d'animaux par page
    offset = (page - 1) * per_page  # Calcul de l'offset en fonction de la page
    app.logger.debug("Pagination", extra={"page":page, "offset": offset})
    animals = (
        Animal.query.limit(per_page).offset(offset).all()
    )  # Sélectionne les animaux pour la page actuelle
    total_animals = (
        Animal.query.count()
    )  # Compte le nombre total d'animaux en base de données
    app.logger.debug("Got the animals from the database !",extra={"number_of_animals":total_animals})
    return render_template(
        "animals.html",
        animals=animals,
        total_animals=total_animals,
        per_page=per_page,
        page=page,
    )


@app.route("/add_animal", methods=["GET", "POST"])
def add_animal():
    error_message = None  # Initialisez la variable du message d'erreur à None
    if request.method == "POST":
        app.logger.debug("Lets add register a new animal in our farm")
        name = request.form["name"]
        animal_type = request.form["type"]
        age = int(request.form["age"])
        try:
            # Tentez de créer une instance de Animal et de l'ajouter à la base de données
            animal = Animal(name=name, type=animal_type, age=age, portions=0)
            db.session.add(animal)
            db.session.commit()
            return redirect("/")
        except IntegrityError as e:
            app.logger.error("Failed to add an animal in the database",extra={"error":e})
            db.session.rollback()  # Annuler la transaction
            # Si l'erreur est due à une violation de contrainte unique, indiquez le champ en erreur
            if "Duplicate" in str(e):
                error_message = "Erreur : Le nom de l'animal doit être unique."
            else:
                error_message = "Erreur lors de l'ajout de l'animal."
            return render_template("add_animal.html", error_message=error_message,animal_list=[el.value for el in AnimalType]), 400

    return render_template(
        "add_animal.html",
        error_message=error_message,
        animal_list=[el.value for el in AnimalType],
    )


@app.route("/animal/<int:animal_id>", methods=["GET"])
def show_animal(animal_id):
    # Remplacez Animal par le nom de votre modèle d'animaux
    animal = Animal.query.get(animal_id)
    if animal is not None:
        return render_template("animal.html", animal=animal)
    else:
        return "Animal non trouvé", 404


@app.route("/feed/<int:animal_id>", methods=["GET"])
def feed_animal(animal_id):
    # Remplacez Animal par le nom de votre modèle d'animaux
    animal = Animal.query.get(animal_id)
    if animal is not None:
        app.logger.info("Feed an animal",extra={"animal_id":animal.id,"animal_type":animal.type.value,"animal_name":animal.name})
        portions, food, message = feedfarmhub_feed(animal.type.value, animal.age)
        # Ajoutez le nombre de croquettes à l'animal
        animal.portions += portions
        # Enregistrez les modifications dans la base de données
        db.session.commit()
        if message == "":
            message = random.choice(messages_repas)

        # Redirigez l'utilisateur vers la page de détails de l'animal
        return render_template(
            "feed.html",
            animal_id=animal_id,
            portions=portions,
            message=message,
            food=food,
        )
    else:
        return "Animal non trouvé", 404
