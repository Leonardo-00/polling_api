## Polls Web Application

This project is a web application that allows users to register, select their favorite categories, create polls with choices, vote on polls, and view poll results.

It is built with **Django REST Framework**, with a frontend that interacts via JSON API.

---

## Features

- User registration and login

For anonymous users:

- retrieving and listing polls and their results

For authenticated users:
- Favorite categories selection (1–3 categories)
- Poll creation (with choices and category)
- Voting (one vote per poll, but can change choice)

# Homepage of the client: https://leonardo-00.github.io/Polling_API_client/home.html

Vercel deployment: https://polling-api-three-rho.vercel.app/

The api is deployed on vercel, the url above is the one where all requests from the client are sent, but it also accepts requests from postman for testing purposes

Authentication is managed using dj-rest-auth, and the user class and serializer have been extended to accept a list of categories on creation and update.

If you want to clone the repo locally, you need to follow these steps:

1) Create a virtualenv: python -m venv venv
2) Activate the venv: venv\Scripts\activate
3) Install dependencies: pip install -r requirements.txt
4) Apply migrations: python manage.py migrate
5) load fixtures: python manage.py:
    python manage.py loaddata dumps/accounts.json
    python manage.py loaddata dumps/categories.json
    python manage.py loaddata dumps/polls.json
    python manage.py loaddata dumps/choices.json
    python manage.py loaddata dumps/votes.json
6) (optional) Create a superuser: python manage.py createsuperuser
7) Start the server: python manage.py runserver








