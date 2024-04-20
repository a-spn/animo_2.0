from app import app
from flask import request, jsonify
from app.anidiet import *
from app.portionpro import *
from app.foodvault import *


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


@app.route("/feed", methods=["GET"])
def feed():
    animal = request.args.get("animal")
    animal_age = request.args.get("age")
    if not animal:
        app.logger.error(
            "Missing parameter 'animal' in the URL",
            extra={"missing_parameter": "animal"},
        )
        return jsonify({"error": "Missing parameter 'animal' in the URL"}), 400

    if not animal_age:
        app.logger.error(
            "Missing parameter 'age' in the URL",
            extra={"missing_parameter": "age"},
        )
        return jsonify({"error": "Missing parameter 'age' in the URL"}), 400

    try:
        animal_age = int(animal_age)
    except ValueError:
        app.logger.error(
            "Parameter 'age' is not an integer", extra={"invalid_parameter": "age"}
        )
        return jsonify({"error": "Parameter 'age' is not an integer"}), 400
    edible_food_for_animal = anidiet_search(animal)
    if len(edible_food_for_animal) == 0:
        app.logger.error("Can't retrieve food for the animal", extra={"animal": animal})
        return jsonify(
            {"error": f"Impossible de trouver la nourriture adaptée pour '{animal}'"}
        )
    for food in edible_food_for_animal:
        required_quantity = portionpro_compute(animal, animal_age, food)
        if required_quantity == -1:
            app.logger.error(
                "Can't estimate food quantity required for the animal",
                extra={"animal": animal, "food": food, "animal_age": animal_age},
            )
            return jsonify(
                {
                    "error": f"Impossible d'estimer la quantité de {food} requise pour un '{animal}' de {animal_age} ans"
                }
            )
        print(food)
        available_quantity = foodvault_search(food)
        if available_quantity >= required_quantity:
            app.logger.info(
                "We have enought food to feed the animal !",
                extra={
                    "animal": animal,
                    "required_quantity": required_quantity,
                    "available_quantity": available_quantity,
                    "food": food,
                },
            )
            return jsonify(
                {"food": food, "animal": animal, "quantity": required_quantity}
            )
        else:
            app.logger.warn(
                "We don't have enough food of this type to feed the animal !",
                extra={
                    "animal": animal,
                    "required_quantity": required_quantity,
                    "available_quantity": available_quantity,
                    "food": food,
                },
            )
    app.logger.error(
        "Oh No, we found nothing to feed this animal",
        extra={
            "animal": animal,
            "edible_food": edible_food_for_animal,
        },
    )
    return (
        jsonify(
            {
                "error": "Pas assez de nourriture pour nourrir cet animal !",
                "animal": animal,
                "edible_food": edible_food_for_animal,
            }
        ),
        500,
    )
