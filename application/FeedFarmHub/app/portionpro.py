import requests
from app import app


def portionpro_compute(animal_type, age, food):
    # Définir les paramètres de l'URL
    params = {
        "animal": animal_type,
        "food": food,
        "age": age,
    }  # Remplacez "lion" par le type d'animal que vous souhaitez rechercher

    # Effectuer la requête GET
    response = requests.get(
        f'{app.config.get("PORTIONPRO_URL")}/portion', params=params
    )
    app.logger.debug("Response content: {}".format(response.text))
    data = response.json()
    # Vérifier la réponse et afficher le contenu
    if response.status_code == 200:
        quantity_required = data["quantity_required"]
        app.logger.info(
            "Required food quantity for the animal successfully retrieved",
            extra={
                "food": food,
                "animal": animal_type,
                "quantity_required": quantity_required,
                "animal_age": age,
            },
        )
        return quantity_required
    else:
        app.logger.error(
            "Unknown error during the request.",
            extra={"status_code": response.status_code, "error": data["error"]},
        )
        return -1
