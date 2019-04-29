# run script to create dynamodb table
    $ sh create.sh 
# run app with auto reload
    $ set FLASK_APP=app.api.py
    $ set FLASK_DEBUG=1
    $ flask run

# endpoints

|request name  |  request value  |
:-------:|:-------:
|get all activities    | _GET/activities_
|create activity       | _POST/activities_
|get activity by id    | _GET/activities/{id}_
|delete by id          | _POST or DELETE/activities/{id}_
|update by id          | _PUT/activities/{id}_

