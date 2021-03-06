# Submit a Fast Stream Post

## Try it out
[This prototype is available to try](https://fast-stream-postings.herokuapp.com/submit/start). Please only select `Data` from the `Job family` page. This may break at any point; if it does, raise an issue here.

## Build
This service is built in Flask. It comprises three containers: a Redis container for storing session data, a Postgres
container for persisting data, and a Python container to run the Flask web server.

To run this locally for yourself, you'll need to install [Docker Compose](https://docs.docker.com/compose/install/).

Once you've installed that (and Docker, if you didn't already have it), clone this repository by typing `git clone https://github.com/jonodrew/fast-stream-postings.git` into your terminal or command prompt. It will output a lot of stuff, and when it's finished type `cd fast-stream-postings` to change directory to the folder. Then run the following command:
`docker-compose up`

This will pull down any Docker images you don't have, so it may take a little while. Once it's finished, it'll launch
the three containers. You should now be able to open your browser, navigate to `localhost:5000/submit/start` and see the
service running.  

If you're using Windows, you may experience [this issue](https://github.com/jonodrew/fast-stream-postings/issues/18). If that happens, run `git config --global core.autocrlf false`

Then delete the folder you downloaded and re-clone it. Once that's done, run `docker-compose up --build`. If that doesn't work, raise an issue and I'll try to help as soon as I can.

When running on Windows 10, docker version 18.06.0-ce  you may experience [this issue](https://github.com/jonodrew/fast-stream-postings/issues/20) when restarting the program after a termination. If this affects you, simply toggle-apply your Docker shared folder off and on in Docker settings as here: ![image](https://user-images.githubusercontent.com/28785439/43518728-dd689ed0-9584-11e8-87ea-824843e446e4.png)
