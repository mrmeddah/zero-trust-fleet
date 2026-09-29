# syntax=docker/dockerfile:1
#
# fleet-app — application Flask de gestion du parc et du carburant.
# L'image est autonome : la base SQLite est creee et peuplee au demarrage
# par database/init_db.py puis database/seed.py.

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    FLEET_DB_DIR=/data

WORKDIR /app

# curl pour le healthcheck, gcc/libldap pour ldap3 si le mode FreeIPA est actif
RUN apt-get update \
 && apt-get install --no-install-recommends -y \
      curl \
      libldap2-dev libsasl2-dev gcc g++ \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Volume de donnees : la base n'est jamais versionnee, elle est regeneree.
RUN mkdir -p /data \
 && adduser --system --group --no-create-home fleet \
 && chown -R fleet:fleet /app /data
USER fleet

EXPOSE 5000

# Genere la base au premier demarrage, puis sert l'application.
CMD ["sh", "-c", "python database/init_db.py && python database/seed.py && exec gunicorn \
      --bind 0.0.0.0:5000 \
      --workers ${GUNICORN_WORKERS:-2} \
      --threads ${GUNICORN_THREADS:-4} \
      --timeout 60 \
      --access-logfile - \
      wsgi:application"]
