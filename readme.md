# Phonebook microservice

## List of resources

###`GET /get-all/` - Get all phones and names

---
###`GET /search/<name>` - Search phone by user name 

***Params:***
```
name - Username. This param is case insensetive
``` 
---
###`POST /add-phone/` - Adds a new phone

***Params:***
```json
{
    "name": "Alex",
    "phone": "+79998883301"
}
``` 
---
###`DELETE /remove-phone/<phone_id>` - Delete phone by id

***Params:***
```
phone_id - The id of the phone
``` 
---

## Installation
1. Install latest version of python and pip
2. Install virtual environment: `python3 -m venv /path/to/new/virtual/environment`
3. Activate virtual environment: 



