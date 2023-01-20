# microservice-django
A microservice blueprint built with python Django

Each service have their separate database completely decoupled. Nginx sits in front of each of the services to abstract all the microservices API endpoints into single one.
#### For first build:
* make setup
#### To run:
* make run
#### To stop:
* make stop


## Technology Stack & Features:
* Django fresh build
* RestFramework
* open API and swagger.
* docker with Docker compose.
* makefile.
* Django signals.
* Logs.
* REDIS
* Celery
* Schedule Tasks (Django Q) 
* Custom exception handler
* message broker - rabbitmq.
* CI/CD Pipeline.
* kubernetes.
* Nginx API-gateway.
* Service registry(Eureka Spring Cloud).
* todo-list app
* Notification Service
* Design patterns (Pub-Sub, Command, Repository, Singleton).
* layer architecture (DDD).
* Frontend
* auth service- keycloak (todo).

# System Architecture:
![System Architecture](https://user-images.githubusercontent.com/15717941/185804170-07e3266b-a0c8-47b2-b0b7-c506731bb45d.jpg)


## Eureka Service:
#### to see all Instances currently registered with Eureka
* URL: http://localhost:8761
<img width="1435" alt="Eureka" src="https://github.com/BekOsu/microservice-django-property-hunt/blob/master/main/static/images/Screenshot%20from%202023-01-20%2018-17-13.png">




## RabbitMq Dashboard:
* URL: http://localhost:15672
* username: guest
* password: guest
<img width="1440" alt="rabbitmq" src="https://github.com/BekOsu/microservice-django-property-hunt/blob/master/main/static/images/Screenshot%20from%202023-01-20%2018-18-32.png">

## Docs:
#### I used OpenAPI with swagger for API docs, also  followed Domain driven design with services Layer architecture to make it easy to understand the code
#### Lastly the Naming of Classes, methods and objects is meaningful.

### to test the APIs see: 
#### http://127.0.0.1:8000/redoc/
#### http://127.0.0.1:8000/swagger/

We used  swager open-API to auto document your APIs

![Screen Shot 2022-07-04 at 2 21 23 PM](https://github.com/BekOsu/microservice-django-property-hunt/blob/master/main/static/images/Screenshot%20from%202023-01-20%2018-21-44.png)

![Screen Shot 2022-07-04 at 2 21 55 PM](https://github.com/BekOsu/microservice-django-property-hunt/blob/master/main/static/images/Screenshot%20from%202023-01-20%2018-20-02.png)

## Communications: 
#### For Async communications I used rabbitmq, and for sync I used normal http calls (later on grpc will be good use).


## Design Patterns:
* Pub-Sub: I used bub-sub model along with events streaming broker rabbitmq.
* Repository: Used repository pattern to decouple Domain layer from DB layer, for example we can mock the repository and use DB memory.
* Singleton: Singleton pattern is used by  django for DBConnections.

## CI/CD:
#### Two steps: Build with tests, then Deploy.
#### I commented the part of pushing the images to DockerHub then uploading it to the cloud but, you can easily uncomment that to make it work.
<img width="1440" alt="Screen Shot 2022-08-21 at 6 37 42 PM" src="https://github.com/BekOsu/microservice-django-property-hunt/blob/master/main/static/images/Screenshot%20from%202023-01-20%2018-24-02.png">

## Todo:
#### the goal was to build the skeleton and base Architecture of the system, but these are Things need to be done when have more time: 
* Review and add more unit, integrations, contracts and acceptance tests.
* Build Frontend with React.js.
* Add more App Validations.
* Focus more on documentation.
* Auth Service with Keycloak.
* REDIS.
* GRPC (support HTTP2/Websocket).

* Note make sure you have Docker installed and give it enough memory from the setting, because we have 6 services running with 4 DBs.
<img width="1440" alt="Screen Shot 2022-08-07 at 3 53 13 PM" src="https://user-images.githubusercontent.com/15717941/183289201-10746be4-af21-4c2e-8242-bf1921c6faef.png">
