import requests
from app import app


def foodvault_search(food):
    # Définir les paramètres de l'URL
    params = {
        "food": food
    }  # Remplacez "lion" par le type d'animal que vous souhaitez rechercher

    # Effectuer la requête GET
    response = requests.get(f'{app.config.get("FOODVAULT_URL")}/search', params=params)
    app.logger.debug("Response content: {}".format(response.text))
    data = response.json()
    # Vérifier la réponse et afficher le contenu
    if response.status_code == 200:
        quantity = data["quantity"]
        app.logger.info(
            "We found food during our search ! ",
            extra={"food": food, "quantity": quantity},
        )
        return quantity
    else:
        app.logger.error(
            "Unknown error during the request.",
            extra={"status_code": response.status_code},
        )
        return -1
