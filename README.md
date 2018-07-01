# Submit a Fast Stream Post

## Build
This service is built in Flask. It comprises three containers: a Redis container for storing session data, a Postgres 
container for persisting data, and a Python container to run the Flask web server. 

To run this locally for yourself, you'll need to install [Docker Compose](https://docs.docker.com/compose/install/).

Once you've install that (and Docker, if you didn't already have it), clone this repo with `git clone`. Then `cd` into 
the folder and run the following command:
`docker-compose up`

This will pull down any Docker images you don't have, so it may take a little while. Once it's finished, it'll launch 
the three containers. You should now be able to open your browser, navigate to `localhost:5000/submit/start` and see the 
service running.  
