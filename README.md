
# Overview - URL Shortening Service

This service, built with Django, offers URL shortening capabilities with advanced tracking and control features. In addition to basic URL shortening, the system includes the following functionalities:

## What it offers

- **Restricted Clicks** -  Allows setting a limit on the total number of clicks a shortened URL can receive. Once the limit is reached, the URL becomes inactive. 

- **Expiration date based Restriction** - You can also provide an date and time after which url would not be valid.

- **Visitors Monitoring** - Tracks data about visitors who use the shortened URLs, such as IP addresses, browser information, geographic location, and timestamps. This provides valuable insights into user behavior and traffic sources

- **URL Management** -  you can monitor the performance of shortened URLs, deactivate them, and track the total number of clicks.

- **Stats report** - you can see which url of yours had generated the most clicks


## How To Setup 

### 1. Setup the virtual environment
### 2. Install the required dependency from `requirements.txt` file 
### 3. Setup the database of your choice, 
by default it uses Postgresql database to keep using it simply provide these configurations in .env file   
```python
POSTGRES_DATABASE_NAME = 'database_name'
POSTGRES_DATABASE_HOST = 'http://database-host.example.com'
POSTGRES_DATABASE_PORT = 5432
POSTGRES_DATABASE_USER = 'database_user'
POSTGRES_DATABASE_PASSWORD = 'database_password'
```
### 4. other configurations
* By default shortened urls identifiers are of length `16`, if you want to make it more shorter or longer you can configure `URL_UNIQUE_IDENTIFIERS_LENGTH` var in `core.settings`.   
You would have to migrate database to reflect this changes, because
Url model uses this setting to set `max_length` of `url` field. 

* You can change endpoints of your choice by changing app's app.urls.urlpatterns 


## How api works
* All data is accepted in json format
* For get requests data should be passed in url string as params 

#### Create an account 
>You would have to create an account by providing email and password parameters.  
>**endpoint** - POST `/api/auth/signup`    
>**accepted parameters** -
>* **email**: required
>* **password**: required

#### Login into existing account   
> **endpoint** - POST `/api/auth/login`    
> **accepted parameters** -
> * **email**: required
> * **password**: required

#### Get Csrf
You need to provide csrf value for each post reqeust. once you get csrf value, it remains same
only need to change if you have created new login or signup. 
You have to pass this value in `X-CSRFToken` header for post requests
> **endpoint** - GET `/api/auth/csrf`    
> **accepted parameters** -


#### Create an shortened url   
> **endpoint** - POST `/api/urls`    
> **accepted parameters** -
> * **url** - required
> * **allowed_visits**
> * **expiration_datetime**

#### Query created urls
> **endpoint** - GET `/api/urls`   
> **accepted paramters** -    
> * **page** 
> * **size** 

#### See the Individual url data 
> **endpoint** - GET `/api/urls/<url_id>`    
> **accepted parameters** -

#### Update an shortened url   
> **endpoint** - PATCH `/api/urls/<url_id>`    
> **accepted parameters** -
> * **expiration_datetime**
> * **allowed_visits**

#### Disable shortened url   
It disabled the url. 
> **endpoint** - POST `/api/urls/<url_id>/disable`    
> **accepted parameters** -

#### Enable shortened url   
> **endpoint** - POST `/api/urls/<url_id>/enable`    
> **accepted parameters** -


#### Query the visitors data    
This endpoint serves the visitors who clicked on the link.
> **endpoint** - GET `/api/urls/<url_id>/visits`    
> **accepted parameters** -
> * **page**
> * **size**

#### See individual visitor detaila   
> **endpoint** - GET `/api/urls/<url_id>/visits/<visitor_id>`    
> **accepted parameters** -

#### Check the top visited sites   
> **endpoint** - GET `/api/urls/stats`    
> **accepted parameters** -
> * **page**
> * **size**
