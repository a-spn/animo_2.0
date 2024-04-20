import requests
from app import app
import json

def feedfarmhub_feed(animal_type, animal_age):
    params = {"animal": animal_type, "age": animal_age}
    response = requests.get(f'{app.config.get("FEEDFARMHUB_URL")}/feed', params=params)
    app.logger.debug("Response content: {}".format(response.text))
    data = response.json()
    # Vérifier la réponse et afficher le contenu
    if response.status_code == 200:
        food = data["food"]
        quantity = data["quantity"]
        app.logger.info(
            "the animal was successfully fed",
            extra={"food": food, "quantity": quantity},
        )
        return (quantity, food, "")
    elif response.status_code == 500:
        return (
            0,
            "",
            f'{data["error"]} Nourriture adaptée pour l\'animal : {data["edible_food"]}',
        )

    return ("", 0, "une erreur inconnue est survenue lors du traitement")
