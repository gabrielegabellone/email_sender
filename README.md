# Email Sender
Project with the aim of learning Django basics.  
Email sender consists of a web app that allows you to send emails to users in a database, just like a newsletter.  
I structured the project in two apps:
- emails: manages the sending of emails (to all subscribers or specific);
- subscribers: deals with CRUD operations of subscribers. Subscribers are the users present in the database, consisting of a username and an email, they cannot log in but can only receive emails.  

All operations can be performed only if you are an admin user.
## Set environment variables
Create a .env file and set the following variables:  
- Needed for sending emails  
```EMAIL_HOST```: is the server that hosts the outgoing SMTP server, for example in the case of Gmail the SMTP host is ```smtp.gmail.com```;  
```EMAIL_PORT```: is the port that defines how the message will be transmitted, so each port supports a different type of encryption, for example port 587 requires a TLS connection;  
```EMAIL_HOST_USER```: the sender's email;  
```EMAIL_PASSWORD```: it's a password you can generate specifically for the app via your email account.
- Needed for database connection: ```MYSQL_DB```, ```MYSQL_USER```, ```MYSQL_PASSWORD```, ```MYSQL_HOST```, ```MYSQL_PORT```.
- ```SECRET_KEY```: it is a cryptographic key, used for example to generate tokens.
## How to run
- install the requirements  
```pip install requirements.txt```
- run the app  
```python manage.py runserver```
- To see the API documentation with swagger UI and test the API go to ```http://localhost:8000/swagger```, or you can go to```http://localhost:8000/swagger.json``` to see it in json format.
## Authentication
Authentication was implemented using the user authentication system provided by Django to manage both authentication and authorizations. To access the API you need to be admin, so the command to create a new superuser is ```python manage.py createsuperuser```.