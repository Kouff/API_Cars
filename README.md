# API Cars

Web framework: AioHTTP.

The repository has branches:
* master (with sqlite3 and without docker)
* with_docker_and_redis (this code but in docker container and using MongoDB instead of sqlite3)

Clone a project and move to it:

    $ git clone https://github.com/Kouff/API_Cars.git
    $ cd API_Cars
Create a [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html#via-pip) and [activate](https://virtualenv.pypa.io/en/latest/user_guide.html#activators) it or skip this point.

Install the requirements:
    
    $ pip install -r requirements.txt
Run server:

    $ python main.py
Requests:
* **POST** http://127.0.0.1:8080/cars/ - create a new car object (the car object has fields: **vin_code**, **manufacturer**, **model**, **year**, **color**).
* **GET** http://127.0.0.1:8080/cars/ - show all the car objects. 
* **GET** http://127.0.0.1:8080/cars/?manufacturer=BMW&model=X5&year_from=1999&year_to=2010&color=yellow - show all the filtered car objects.
* **GET** http://127.0.0.1:8080/cars/{code}/ - show a car objects (**code** is a car vin_code). 
* **PATCH** http://127.0.0.1:8080/cars/{code}/ - update fields in a car objects (**code** is a car vin_code). 
* **DELETE** http://127.0.0.1:8080/cars/{code}/ - delete a car objects (**code** is a car vin_code). 
