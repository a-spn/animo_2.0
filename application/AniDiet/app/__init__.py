from flask import Flask
from logging.config import dictConfig
import os

app = Flask(__name__)

app.config.update(
    TESTING=False,
    DEBUG=False,
    SECRET_KEY="192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf",
    SESSION_TYPE="filesystem",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,  # Désactive le suivi des modifications de la base de données
)

from opentelemetry.instrumentation.flask import FlaskInstrumentor

FlaskInstrumentor().instrument_app(app, excluded_urls="/metrics")

from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app, group_by="endpoint")
metrics.info("flask_info", "Application info", version="1.0.3")


from app import logs, routes, constants

# Configuration de la journalisation avec dictConfig
log_config = {
    "version": 1,
    "formatters": {
        "json": {"()": logs.JsonFormatter},
    },
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "formatter": "json",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["wsgi"],
    },
}


dictConfig(log_config)
