# Submit a Fast Stream Post

## Build
This service is built in Flask. It uses a Docker container. 
Before you start, you'll need a database and a way for the container to access it. In Flask, this is done by setting 
the environment variable `DATABASE_URL`. If you don't set it, the container will look for a locally hosted database,
which it won't find.

This can be done by creating a database container or by using a cloud-based database. I used Heroku, because I was 
planning to deploy the prototype there anyway.

Therefore to build this service you'll need:

- a database
- Docker installed on your local machine 
