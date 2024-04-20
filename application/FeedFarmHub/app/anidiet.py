import requests
from app import app


def anidiet_search(animal_type):
    # Définir les paramètres de l'URL
    params = {
        "animal_type": animal_type
    }  # Remplacez "lion" par le type d'animal que vous souhaitez rechercher

    # Effectuer la requête GET
    response = requests.get(f'{app.config.get("ANIDIET_URL")}/search', params=params)
    app.logger.debug("Response content: {}".format(response.text))
    # Vérifier la réponse et afficher le contenu
    if response.status_code == 200:
        data = response.json()
        food = data["food"]
        app.logger.info("Food retrieved successfully", extra={"food": food})
        return food
    elif response.status_code == 404:
        error_data = response.json()
        app.logger.error(
            "Animal not found",
            extra={"animal_type": animal_type, "error": error_data["error"]},
        )
    else:
        app.logger.error(
            "Unknown error during the request.",
            extra={"status_code": response.status_code},
        )
    return []