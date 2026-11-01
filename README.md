# fullstack_developer_capstone

Best Cars dealership portal based on the IBM Full Stack Developer Capstone starter.

## Features

- React registration, login/logout and dealership directory with state filtering
- Dealer details, sentiment-labelled reviews, and authenticated review submission
- Django proxy API, session authentication, CSRF protection and car catalog administration
- Express/Mongoose API with persistent MongoDB data, non-destructive seed loading and atomic review IDs
- NLTK VADER sentiment analysis using the included lexicon
- Container definitions for all services and GitHub Actions checks

## Run with Docker Compose

Create an untracked `.env` file containing a random `DJANGO_SECRET_KEY`. For a hosted instance also set `DJANGO_ALLOWED_HOSTS` to its hostname and `DJANGO_CSRF_ORIGINS` to its full HTTPS origin.

```sh
docker compose up -d --build
docker compose exec web python manage.py createsuperuser
```

The web app runs on port 8000, the dealership API on 3030, and sentiment analysis on 5050. Port mappings bind to loopback by default. MongoDB is available only on the private Compose network.

Seeded vehicle makes and models are added on web-service startup. Review and dealership data are seeded only when the respective collection is empty.

## Validation

```sh
pip install -r server/requirements.txt
python server/manage.py test djangoapp
npm ci --prefix server/frontend
npm run build --prefix server/frontend
```

The tests cover authentication, password hashing, CSRF enforcement, review author identity, state filtering and vehicle catalog serialization. GitHub Actions repeats the tests and builds the web container.

## Assessment evidence

Screenshots are captured from the running application and stored locally in `output/evidence/`. Review the implementation and course rules before submitting. This project was implemented with AI assistance.
