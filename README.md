# MY API

This example vanilla project to start REST API project

| Environment | URL | Build status | Coverage |
| ----------- | --- | -------- | -------- |

| Dev  | [http://localhost:5002/](http://localhost:5002/) | -- | -- |


##Requirements
@see [configs/requirements.txt](/configs/requirements.txt)
When you change file requirements.txt please remember to rebuild docker container
```bash
docker-compose up --build
```

## How to setup DEV environment?
- Go to folder where you would like to keep code and clone repo from  GITLAB
```
cd {your_code_directory}
git clone git@github.com:TaQba/my_api.git
cd my_api
```
- First time, build docker composer (first build or rebuild only)
```
docker-compose up --build
```

- Setup DB - login to container and run script
```
you@yourmachine$ docker exec -it my_api bash
root@xxx:/code# ./bin/setup_db.sh 
```


## How to add new ENDPOINT?
@see [https://flask-restful.readthedocs.io]

1. add controller class in /core/controllers ie. test.py 
2. add router class in /core/routers ie.test.py with methods like get|post|put|delete and including @jwt_required() if needed. There methods should be simple (no business logic here) and point to controller methods
3. add endpoint in /app.py with specifying GET params if needed doing a basic cast validation ie.  

```
api.add_resource(User, '/tests', '/tests/<int:user_id>')
```

Please follow of example for endpoint users [/users]


## How to run test on DEV environment?
docker container is named 'my_api'
```
you@yourmachine$ docker exec -ti my_api bash 
root@xxx:/code# $ ./bin/run-tests.sh
```
'run-tests.sh' runs all tests in test_*.py files under /tests/unit
'run-single-test.sh' runs the specified test


## How to run app on you dev machine?

Use Postman application to run REST requests
You can find configuration file in {project}/postman and import this file into Postman app.


## How to create migration file?
- create new model or update existing one
- run migrate command ``flask db migrate -m "Some message"``
- update migrate file if necessary
- run command ``flask db upgrade`` to update your DB

## How to see DB schema (models)
- use MYSQL_WORKBENCH model from folder mysql_workbench
- every DB changes should be also included in this model


## How track logs
```bash
tail -f -n300 /var/log/supervisor/supervisord.log 
```
