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



@app.route("/search", methods=["GET"])
def search_food():
    food_name = request.args.get("food")
    app.logger.debug("new search !", extra={"food_name": food_name})
    if food_name not in all_animal_foods:
        return (
            jsonify(
                {"error": "Cette nourriture n'existe pas"},
            ),
            404,
        )
    if 20 >= random.randint(
        0, 100
    ):  # 20% de chance qu'il n'y ait plus de cette nourriture
        return (
            jsonify(
                {
                    "error": "Cette nourriture n'est plus disponible",
                    "food_name": food_name,
                    "quantity": 0,
                }
            ),
            200,
        )
    quantity = random.randint(1, 7)
    return jsonify(
        {
            "food_name": food_name,
            "quantity": quantity,
        }
    )


@app.route("/", methods=["GET"])
def index():
    mapping_food_quantity = {}
    for food in all_animal_foods:
        mapping_food_quantity[food] = random.randint(0, 5)
    return jsonify(mapping_food_quantity)
