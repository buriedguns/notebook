# Phonebook microservice

## List of resources

`GET /get-all/` - Get all phones and names

---
`GET /search/<name>` - Search phone by user name 

***Params:***
```
name - Username. This param is case insensetive
``` 
---
`POST /add-phone/` - Adds a new phone

***Params:***
```json
{
    "name": "Alex",
    "phone": "+79998883301"
}
``` 
---
`DELETE /remove-phone/<phone_id>` - Delete phone by id

***Params:***
```
phone_id - The id of the phone
``` 
---

## Install and run the app

* Install latest version of python and pip
* Install virtual environment: 
```
pip3 install virtualenv
cd my-project/
virtualenv venv
```


* Activate virtual environment: 

```source venv/bin/activate```
* Install all required packages:

```pip install -r requirements.txt```

## Run tests
* Activate the same virtual environment in another terminal:

```source venv/bin/activate```

* Run all tests:

```pytest```



