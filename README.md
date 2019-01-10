[![Build Status](https://travis-ci.org/Benkimeric/iReporter-API.svg?branch=bg-fix-travis-162329458)](https://travis-ci.org/Benkimeric/iReporter-API)     [![Coverage Status](https://coveralls.io/repos/github/Benkimeric/iReporter-API/badge.svg?branch=develop)](https://coveralls.io/github/Benkimeric/iReporter-API?branch=develop)    [![Maintainability](https://api.codeclimate.com/v1/badges/3342f24d82c1a9a9a645/maintainability)](https://codeclimate.com/github/Benkimeric/iReporter-API/maintainability)

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/22f76cf257cd08364284)

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


### V2 Features Endpoints:
| Method | Route | Endpoint Functionality |
| :---         |     :---       |          :--- |
| POST     | /api/v2/auth/signup        | Register a new user to the application     |
| POST     | /api/v2/auth/login        | Login a user to the application      |
| GET     | /api/v2/red-flag        | View All Red-flags     |
| POST     | /api/v2/red-flag        | Add an Incident Record      |
| GET     | /api/v2/red-flag/incident_id       | Retrieve a single red-flag     |
| DELETE     | /api/v2/red-flag/incident_id       | Delete a single red-flag by id     |
| PATCH     | /api/v2/ red-flag/incident_id/comment     | Edit a red-flag comment by ID    |
| PATCH     | /api/v2/ red-flag/incident_id/location     | Edit a red-flag location by ID    |
| POST     | /api/v2/intervention       | Add an Incident Record      |
| GET     | /api/v2/intervention/incident_id       | Retrieve a single intervention     |
| DELETE     | /api/v2/intervention/incident_id       | Delete a single intervention by id     |
| PATCH     | /api/v2/ intervention/incident_id/comment     | Edit a intervention comment by ID    |
| PATCH     | /api/v2/ intervention/incident_id/location     | Edit a intervention location by ID    |
| PATCH     | /api/v2/makeadmin/user_id        | Promote a user to an admin by their ID      |
| GET     | /api/v2/users/        | View all the registered users      |
| GET     | /api/v2/users/user_id        | View details of a registered user      |
| GET     | /api/v2/user/red-flag/        | View all red-flags by a certain user      |
| GET     | /api/v2/user/intervention/        | View all interventions by a certain user      |

### Installation Procedure
download and install python3

clone the repo

``` 
git clone https://github.com/Benkimeric/iReporter-API.git

```

create and activate the virtual environment

```
virtualenv <environment name>

```
```
$source <environment name>/bin/activate (in bash)

```
install project dependencies using:

```
$pip install -r requirements.txt

```
### Running
Running the application
```
python run.py or flask run

```
### Testing
Using pytest run following command while in the folder containing the application
```
pytest -v

```
Testing can also be done using postman, 
```
python run.py or flask run

Then in python navigate to http://127.0.0.1:5000/ and test the above endpoints

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