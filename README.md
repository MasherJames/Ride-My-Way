![license](https://img.shields.io/github/license/mashape/apistatus.svg)
[![Build Status](https://travis-ci.org/MasherJames/Ride-My-Way.svg?branch=ch-challenge-two-develop-158460445)](https://travis-ci.org/MasherJames/Ride-My-Way)
[![Coverage Status](https://coveralls.io/repos/github/MasherJames/Ride-My-Way/badge.svg?branch=ch-challenge-two-develop-158460445)](https://coveralls.io/github/MasherJames/Ride-My-Way?branch=ch-challenge-two-develop-158460445)

# Ride-My-Way

Ride-my-way App is a carpooling application that provides drivers with the ability to create ride offers
and passengers to join available ride offers.

### _Home page_

![Home page](ui/static/images/home-page-header.png)

**How it works**

- A driver creates an account and logs in
- The driver creates ride offers
- A passenger creates an account and logs in
- A passenger is able to view all available ride offers and can request to join
- The driver accepts or rejects the request from the passenger
- The passenger is notified about the response

### _How it works_

![How it works](ui/static/images/home-page-works.png)

**Installation**

```
git clone git@github.com:MasherJames/Ride-My-Way.git
```

- cd Ride-My-Way/ui
- Open `index.html` in your favorite browser

# API

## _Prerequisites_

- Python 3.6
- Flask
- Flaskrestfull
- Virtualenv

## _Enviroment variables_

- Secret key
- Postgres database url

**Testing**

```
git clone -b ch-challenge-two-develop-158460445 git@github.com:MasherJames/Ride-My-Way.git
```

**Running the app**

```
export FLASK_APP = run.py
export MODE = development

flask run
```

## Endpoints to test

| Method | Endpoint                        | Description                                    |
| ------ | ------------------------------- | ---------------------------------------------- |
| POST   | /api/v1/auth/signup             | sign up a user                                 |
| POST   | /api/v1/auth/login              | login a user                                   |
| POST   | /api/v1/rides                   | post a ride offer                              |
| GET    | /api/v1/rides                   | get all ride offers                            |
| GET    | /api/v1/rides/<rideId>          | get a specific ride offer depending on it's id |
| POST   | /api/v1/rides/<rideId>/requests | request to join a specific ride offer          |
| DELETE | /api/v1/rides/<rideId>          | delete a specific ride offer                   |

### Languages and tools used

- HTML5
- CSS3
- Python/Flask
- Git and Github
- Pivotal tracker

### Author

James Macharia

### Acknowledgement

Andela Bootcamp 29
