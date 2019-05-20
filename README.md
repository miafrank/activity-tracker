## configure aws cli
    $ aws configure

## run script to create dynamodb table
    $ sh create.sh 
## install python packages
    $ pipenv install
## install node packages
    $ npm install
## activate virtual env
    $ pipenv shell
## run app with auto reload
    $ set FLASK_APP=app.api.api.py
    $ set FLASK_DEBUG=1
    $ flask run

## endpoints

|request name  |  request value  |
:-------:|:-------:
|get all activities    | _GET/activities_
|create activity       | _POST/activities_
|get activity by id    | _GET/activities/{id}_
|delete by id          | _POST or DELETE/activities/{id}_
|update by id          | _PUT/activities/{id}_


### tech stack
+ language: python 3.7
+ api framework: flask 1.0.2
+ unit testing frameworks: pytest, unittest, moto
+ database: aws dynamodb