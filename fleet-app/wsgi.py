"""Point d'entrée WSGI pour gunicorn : gunicorn -w 2 -b 0.0.0.0:5000 wsgi:application
"""
from app import creer_app

application = creer_app()