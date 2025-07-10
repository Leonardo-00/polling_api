# Polls Web Application

This project is a web application that allows users to register, select their favorite categories, create polls with choices, vote on polls, and view poll results.

It is built with **Django REST Framework**, with a frontend that interacts via JSON API.

Authentication is managed using dj-rest-auth, and the user class and serializer have been extended to accept a list of categories on creation and update.

# Features

- User registration and login

For anonymous users:

- retrieving and listing polls and their results

For authenticated users:
- Favorite categories selection (1–3 categories)
- Poll creation (with choices and category)
- Voting (one vote per poll, but can change choice)
- Editing user info and favorite categories

# Vercel deployment: 

https://polling-api-three-rho.vercel.app/

The api is deployed on vercel, the url above is the one where all requests from the client are sent, but it also accepts requests from postman for testing purposes

# Local installation

If you want to clone the repo locally, you need to follow these steps:

1) Create a virtualenv: python -m venv venv
2) Activate the venv: venv\Scripts\activate
3) Install dependencies: pip install -r requirements.txt
4) Apply migrations: python manage.py migrate
5) load fixtures: python manage.py:
    - python manage.py loaddata dumps/accounts.json
    - python manage.py loaddata dumps/categories.json
    - python manage.py loaddata dumps/polls.json
    - python manage.py loaddata dumps/choices.json
    - python manage.py loaddata dumps/votes.json
6) (optional) Create a superuser: python manage.py createsuperuser
7) Start the server: python manage.py runserver

To then use the client just open one of the .html files in the Client folder in the project

---

# Endpoints

## CRUD

Endpoint |HTTP Method | CRUD Method | Result | Authentication required | Ownership required
-- | -- |-- |-- |-- | --
`api/polls/` | GET | READ | Get all polls | X | X 
`api/polls/<id>` | GET | READ | Get a single poll | X | X
`api/polls/`| POST | CREATE | Create a new poll | O | -
`api/polls/<id>` | PATCH | UPDATE | Update a poll | O | O
`api/polls/<id>` | DELETE | DELETE | Delete a poll | O | O
`api/polls/vote/<id>` | GET | READ | Get a list of all votes for selected poll | X | X
`api/polls/vote/<id>` | POST | CREATE | Adds (or updates*) a vote for selected poll | X | X
`api/polls/<id>/results/` | GET | READ | Get all the info about selected poll: details, choices and # of votes for each | X | X
`api/users/profile/` | GET | READ | Get the details of a user| O | -
`api/users/profile/` | PATCH | UPDATE | Update user details | X | X

 *(the view checks that a vote by the user on the selected poll already exists and updates that one, not creating a second one) 

## Queries and filters

Endpoint |HTTP Method | Result | Authentication required | Ownership required
-- | -- |-- |-- | --
`api/polls/?category=<category_name>` | GET | Get all polls of selected category | X | -
`api/polls/?username=<username>` | GET | Get all polls of selected user | X | -
`api/polls/?interest=true`| GET | Get all polls of the categories of interest of the user | O | -
`api/polls/categories/` | GET | Get a list of all the categories | X | -
`api/users/whoami/` | GET | Returns the username of the user, used as a check for authentication | O | O


# Use

## Github hosting

The main way to use the API is through a client deployed on github: https://leonardo-00.github.io/Polling_API_client/home.html

## Postman

As written above, https://polling-api-three-rho.vercel.app/ is the public url for endpoints of the API

# Examples of requests with inputs and expected outputs

## Retrieve polls

Input
```
http GET https://polling-api-three-rho.vercel.app/api/polls/
```
Output
```
[
    {
        "id": <id>,
        "question": "question",
        "created_by": 1,
        "created_at": "2025-07-10T14:35:57.303680Z",
        "category": "Clothing",
        "created_by_username": "leona",
        "choices": [
            {
                "id": 70,
                "text": "example",
                "poll": 25
            },
            {
                "id": 71,
                "text": "example",
                "poll": 25
            },
            {
                "id": 72,
                "text": "example",
                "poll": 25
            }
        ]
    },
    ...
]
```

## Retrieve selected poll

Input
```
http GET https://polling-api-three-rho.vercel.app/api/polls/<id>/
```
Output
```
Same as above, but just one instead of a list
```

## Create poll

Input
```
http POST https://polling-api-three-rho.vercel.app/api/polls/ "Authorization: Token 'TOKEN'" question="question" category="category_name" choices=["choice1", "choice2", ...]
```
Output
```
Same as above
```

## Update poll

This also manages the choices in the poll. (creation/update/deletion)

The fields "question" and "category" are optional, and won't be modified if not present.

The list "choices" is mandatory, but can be empty.

A few example of choice elements in the "choices" list is:

New choice
```
{
    text: "choice_text",
    new: true
}
```
Existing choice to be modified
```
{
    id: <id>,
    text: "new_text"
}
```
Existing choice to be deleted
```
{
    id: <id>,
    delete: true
}
```

If a choice doesn't align with any of the examples above it will be ignored

A full request example may be:
```
http PATCH https://polling-api-three-rho.vercel.app/api/polls/<id>/    "Authorization: Token 'TOKEN'" 
                                                                        question="new question" 
                                                                        choices=[{text: "choice_text", new: true}, {id: <id> delete:true}]
```

## Delete poll

This will also (obviously) automatically delete all the choices of the poll and all the votes

Input
```
http DELETE https://polling-api-three-rho.vercel.app/api/polls/<poll_id>/ "Authorization: Token 'TOKEN'"
```

## Retrieving votes of a poll

Input
```
http GET https://polling-api-three-rho.vercel.app/api/polls/vote/<poll_id>/
```
Output
```
[
    {
        "id": 16,
        "poll": 18,
        "poll_question": "example question",
        "choice": 47,
        "choice_text": "example text",
        "voted_by": 8,
        "voted_by_username": "example username"
    },
    ...
]
```

## Creating/updating a vote on a poll

If the user of the request is the author of the poll the vote will get rejected

Input
```
http POST https://polling-api-three-rho.vercel.app/api/polls/vote/<poll_id>/ "Authorization: Token 'TOKEN'" option_id: <id>
```
Output
```
message = "Vote registered."
```
or on update
```
message = "Vote updated."
```

## Retrieving poll results

Input
```
http GET https://polling-api-three-rho.vercel.app/api/polls/<id>/results/
```
Output
```
{
    "poll_id": 18,
    "question": "example",
    "choices": [
        {
            "id": 46,
            "text": "example",
            "votes": 2,
            "voted": true
        },
        {
            "id": 47,
            "text": "example",
            "votes": 2,
            "voted": false
        }
    ]
}
```

Here the field "voted", which is a boolean, only gets added if the user is authenticated, otherwise it is missing

## Retrieve user details

Input
```
http GET https://polling-api-three-rho.vercel.app/api/users/profile/ "Authorization: Token 'TOKEN'"
```
Output
```
{
    "id": 1,
    "username": "example",
    "email": "example",
    "first_name": "example",
    "last_name": "example",
    "favorite_categories": [
        "example",
        "example"
    ]
}
```
## Edit user details

If the request has more than 3 categories it will be rejected

All the fields are also not required

Input
```
http PATCH https://polling-api-three-rho.vercel.app/api/users/profile/ "Authorization: Token 'TOKEN'" 
```
Output
```
Same as above, just updated with modified fields
```

## Filters for poll retrieving

The endpoint api/polls/ accepts the following filters:
```
interest=true
```
Which requires authentication and yields all the polls of the categories of interest to the user
```
username="name"
```
Which yields all the polls created by the selected user, giving error if no user with the provided name exists

```
category="name"
```
Which yields all polls of selected category, giving error if no category with provided name exists

## Retrieving categories list

Input
```
http GET https://polling-api-three-rho.vercel.app/api/polls/categories/
```
Output
```
[
    {
        "name": "example"
    },
    {
        "name": "example"
    },
    {
        "name": "example"
    },
    ...
]
```

This is not a pure list of strings to stay open to extension of the Category model, which could include other fields

## Whoami

This endpoint only stands as a check for the front end to secure the token in the localStorage is real

The response will contain the username of the authenticated user if the check is passed, otherwise Unauthorized error

Input
```
http GET https://polling-api-three-rho.vercel.app/api/users/whoami/ "Authorization: Token 'TOKEN'"
```
Output
```
{
    "username": "name"
}
```