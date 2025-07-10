## Polls Web Application

This project is a web application that allows users to register, select their favorite categories, create polls with choices, vote on polls, and view poll results.

It is built with **Django REST Framework**, with a frontend that interacts via JSON API.

---

## Features

- User registration and login
- Favorite categories selection (1–3 categories)
- Poll creation (with choices and category)
- Voting (one vote per poll, but can change choice)
- Poll result statistics
- Admin interface

# Homepage of the client: https://leonardo-00.github.io/Polling_API_client/home.html

Vercel deployment: https://polling-api-three-rho.vercel.app/
The api is deployed on vercel, the url above is the one where all requests from the client are sent, but it also accepts requests from postman for testing purposes

Authentication is managed using dj-rest-auth, and the user class and serializer have been extended to accept a list of categories on creation and update.

Below is a list of the main API endpoints, their HTTP methods, and the expected JSON input/output formats.







