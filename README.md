Homepage of the client: https://leonardo-00.github.io/Polling_API_client/home.html

Vercel deployment: polling-api-project.vercel.app

The api offers endpoints for

1) Retrieving polls, with a list of all the polls, and a list of the polls of a user, only for authenticated users
2) Creating and editing polls, only for authenticated users
3) Retrieving polls results for all users and voting only for authenticated ones
  
The authenticated user can choos between 1 and 3 favorite categories on registration, and in the homepage, once authenticated, can see a list of polls of his favorite categories

When a user edits a poll, editing a choice, all the votes to that choice will be deleted
