from app import app
from flask import request, jsonify
from app.constants import *
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


@app.route("/portion", methods=["GET"])
def compute_portion():
    animal = request.args.get("animal")
    food = request.args.get("food")
    animal_age = request.args.get("age")

    if not animal:
        app.logger.error(
            "Missing parameter 'animal' in the URL",
            extra={"missing_parameter": "animal"},
        )
        return jsonify({"error": "Il manque le paramêtre 'animal' dans la requête"}), 400

    if not food:
        app.logger.error(
            "Missing parameter 'food' in the URL", extra={"missing_parameter": "food"}
        )
        return jsonify({"error": "Il manque le paramêtre 'food' dans la requête"}), 400

    if not animal_age:
        app.logger.error(
            "Missing parameter 'age' in the URL",
            extra={"missing_parameter": "age"},
        )
        return jsonify({"error": "Il manque le paramêtre 'âge' dans la requête"}), 400

    try:
        animal_age = int(animal_age)
    except ValueError:
        app.logger.error(
            "Parameter 'age' is not an integer", extra={"invalid_parameter": "age"}
        )
        return jsonify({"error": "Parameter 'age' is not an integer"}), 400

    app.logger.debug("New portion calculation", extra={"animal": animal, "food": food})
    quantity = random.randint(2, 9)
    return jsonify({"food": food, "animal": animal, "quantity_required": quantity})
