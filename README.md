[![Build Status](https://travis-ci.org/Benkimeric/iReporter-API.svg?branch=bg-fix-travis-162329458)](https://travis-ci.org/Benkimeric/iReporter-API)     [![Coverage Status](https://coveralls.io/repos/github/Benkimeric/iReporter-API/badge.svg?branch=develop)](https://coveralls.io/github/Benkimeric/iReporter-API?branch=develop)    [![Maintainability](https://api.codeclimate.com/v1/badges/3342f24d82c1a9a9a645/maintainability)](https://codeclimate.com/github/Benkimeric/iReporter-API/maintainability)

# iReporter-API
```
iReporter is an application to report corruption and inform government on things it should intervene.
```

### Tech/ Framework Used

``` 
Python / Flask

```



### V1 Features Endpoints:
| Method | Route | Endpoint Functionality |
| :---         |     :---       |          :--- |
| GET     | /api/v1/red-flags        | View All Incidences     |
| POST     | /api/v1/red-flags        | Add an Incident Record      |
| GET     | /api/v1/red-flags/record_id       | Retrieve a single incident by id     |
| DELETE     | /api/v1/red-flags/record_id       | Delete a single incident by id     |
| PATCH     | /api/v1/ red-flags/record_id/comment     | Edit an incident comment by ID    |
| PATCH     | /api/v1/ red-flags/record_id/location     | Edit an incident location by ID    |


### Installation Procedure
clone the repo

``` 
git clone https://github.com/Benkimeric/iReporter-API.git

```

create and activate the virtual environment

```
virtualenv <environment name>

```
```
$source <env name>/bin/activate (in bash)

```
install project dependencies:

```
$pip install -r requirements.txt

```
### Running
Running the application
```
python run.py

```
### Testing
Using pytest . The tests are in app/api/tests/v1
```
pytest -v

```
### Deployment
The app is deployed using  Heroku at:

```
https://ireporter-api-heroku.herokuapp.com/

```
### Owner
Developed By:

```
Eric Kimeu Bernard