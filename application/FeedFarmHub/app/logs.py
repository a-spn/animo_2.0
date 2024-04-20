import logging
import json
import time

excluded_fields = [
    "filename",
    "funcName",
    "module",
    "name",
    "msecs",
    "excluded_fields",
    "args",
    "levelno",
    "pathname",
    "exc_info",
    "exc_text",
    "lineno",
    "created",
    "thread",
    "relativeCreated",
    "threadName",
    "processName",
    "process",
]
ordered_fields = ["levelname", "msg"]


# Créez une classe de formateur personnalisée pour générer des logs en JSON avec des données supplémentaires
class JsonFormatter(logging.Formatter):
    def format(self, record):
        new_record = {"timestamp":time.time()}

        if "filename" in record.__dict__ and "funcName" in record.__dict__:
            new_record[
                "function"
            ] = f"{record.__dict__['filename']}:{record.__dict__['funcName']}"

        # Exclure les champs spécifiés et les champs vides ou nuls
        for field in ordered_fields:
            if (
                field in record.__dict__
                and record.__dict__[field] is not None
                and record.__dict__[field] != ""
            ):
                new_record[field] = record.__dict__[field]

        # Ajoutez tous les autres champs du dictionnaire
        for key, value in record.__dict__.items():
            if (
                key not in new_record
                and key not in excluded_fields
                and value is not None
                and value != ""
            ):
                new_record[key] = value

        return json.dumps(new_record)