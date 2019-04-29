# run script to create dynamodb table
    $ sh create.sh 
# run app with auto reload
    $ set FLASK_APP=app.api.py
    $ set FLASK_DEBUG=1
    $ flask run

# endpoints

|request name  |  request value  |
:-------:|:-------:
|get all activities    | _/GET/activities_
|create activity       | _/POST/activities_
|get activity by id    | _/GET/activities/{id}_
|delete by id          | _/POST or DELETE/activities/{id}_
|update by id          | _/PUT/activities/{id}_

