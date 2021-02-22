# API Cars

Web framework: AioHTTP.

Clone the project and move to it:

    $ git clone https://github.com/Kouff/API_Cars.git
    $ cd API_Cars
    $ git checkout with_docker_and_mongodb
Build and run docker container:
    
    $ docker-compose up -d --build
Requests:
* **POST** http://127.0.0.1:8080/cars/ - create a new car object (the car object has fields: **vin_code**, **manufacturer**, **model**, **year**, **color**).
* **GET** http://127.0.0.1:8080/cars/ - show all the car objects. 
* **GET** http://127.0.0.1:8080/cars/?manufacturer=BMW&model=X5&year_from=1999&year_to=2010&color=yellow - show all the filtered car objects.
* **GET** http://127.0.0.1:8080/cars/<code>/ - show a car objects (**code** is a car vin_code). 
* **PATCH** http://127.0.0.1:8080/cars/<code>/ - update fields in a car objects (**code** is a car vin_code). 
* **DELETE** http://127.0.0.1:8080/cars/<code>/ - delete a car objects (**code** is a car vin_code).

Stop docker container:
    
    $ docker-compose down
