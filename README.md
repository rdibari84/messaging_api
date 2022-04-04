## Messaging API

### Requirements For Running
- Docker Desktop is installed on your machine
  - You Can Install DockerDesktop [here](https://docs.docker.com/desktop/mac/install/)
  
### To Run
1. Clone Repo
2. Run
  ```
  cd messaging_api
  docker-compose up --build -d --force-recreate
  ```
  - Note: Takes ~ 4 mins to start running
  - Stands up the API Server at `http://localhost:8000`
  - Stands a postgres database at `psql -U postgres -h 0.0.0.0`
  - Seeds the database with data from `db_init.sql`

### To stop
```
docker-compose down
# To fully clean up
docker system prune -a 
```


## Endpoints
### GET /users - Lists All Users
```
curl -X GET http://localhost:8000/api/users 
```
### GET /message/{user_name} - Lists All Messages for a user
- defaults to returning messages no older than 30 days
- TODO: make configurable
```
curl -X GET http://localhost:8000/api/messages/rdibari
curl -X GET http://localhost:8000/api/messages/fakeuser
```
### POST /messages - Send a Message
- It really just saves a message to the database
```
curl -X POST http://localhost:8000/api/messages -H 'Content-Type: application/json'  -d '{"sender_user_name":"rdibari","recipient_user_name":"bugs","body":"hey"}'
```

## Discussion

### Data Model
- Messages
  - id integer DEFAULT nextval('messaging.messaging_sequence'::regclass) NOT NULL, 
  - sender_id INT NOT NULL, 
  - recipient_id INT NOT NULL, 
  - body text NOT NULL, 
  - created_at TIMESTAMP, 
  - timestamp_sent TIMESTAMP,
  - timestamp_delivered TIMESTAMP,
  - timestamp_read TIMESTAMP,
  - FOREIGN KEY (sender_id) REFERENCES messaging.users (id),
  - FOREIGN KEY (recipient_id) REFERENCES messaging.users (id)

- Users
  - id serial PRIMARY KEY,
  - first_name varchar(32),
  - last_name varchar(32),
  - user_name UNIQUE varchar(32),
  - email UNIQUE varchar(254),
  - mfa BOOLEAN NOT NULL,
  - created_at TIMESTAMP,
  - modified_at TIMESTAMP

OF NOTE:
- Created an index on users.user_name, since that is a common access pattern
- Created a sequence on Messages to easily insert new records

### Notable exceptions
- NO pagination
- Minimal Error Handling and Logging
- Obvious Endpoints missing such as
  - Authenication
  - asserting friends
  - group messages
  - emoji & gif support
  
### Technologies
- fastapi - FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints
- uvicorn - the ASGI server we'll use to serve up our app
- pydantic - validation library baked into fastapi that we'll use to handle data models at different stages throughout our application
- databases - An async interface to a number of popular databases.
- SQLAlchemy - The most well known SQL toolkit for Python. Many apps employ this package as an ORM, but we'll writing our database queries in raw SQL, so we'll use it simply for managing database tables.

### Code Structure
```
|-- backend
|   |-- app
|       |-- api
|           |-- routes.py
|           |-- server.py
|       |-- db
|           |-- connections.py
|           |-- repos.py
|       |-- models
|           |-- models.py
|       | config.py
|   |-- .env
|   |-- Dockerfile
|   |-- requirements.txt
|-- .gitignore
|-- docker-compose.yml
|-- db_init.sql
|-- README.md
```

### Other Notes  
- To see logs
```
docker logs -f messaging_api_server_1
docker logs -f messaging_api_db_1
```