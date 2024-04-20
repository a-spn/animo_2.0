from app import app
from flask import request, jsonify
from app.constants import *


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


@app.route("/search", methods=["GET"])
def search_animal():
    animal_type = request.args.get("animal_type")
    app.logger.debug("new search !", extra={"animal_type": animal_type})
    if animal_type in mapping_animal_food:
        app.logger.debug("Animal found in the mapping", extra={"animal_type": animal_type})
        food_list = mapping_animal_food[animal_type]
        app.logger.info(
            "food succesfully retrieved",
            extra={"food": str(food_list), "food_number": len(food_list)},
        )
        response = {"animal_type": animal_type, "food": food_list}
        return jsonify(response), 200
    else:
        app.logger.error(
            "Animal not found in the mapping.",
            extra={"animal_type": animal_type},
        )
        return jsonify({"error": "L'animal n'existe pas dans le référentiel AniDiet"}), 404


@app.route("/", methods=["GET"])
def index():
    return jsonify(mapping_animal_food)
