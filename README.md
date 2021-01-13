# NS Covid Case watcher


I build this project because I wanted to keep track of all the new cases that were being announced and get the new count send to me via email


# Docker .env files

There are 2 file that need to be created.

- .env-email
   - PASSWD :
        Email account password for Gmail
   - SENDER_EMAIL :
        Email address for the account

- .env-database
   - DATABASE_CONNECTION_PASSWORD : 
        PostgresQL database password
   - POSTGRES_USER : 
        Username for the PostgresQL database



# DB schema

Here is the DB schema because in order to use this project

| name (String/VarChar) | email (String/VarChar) | hasEmailBeenSentToday (Boolean) |
| ------ | ------ | ------ |
| Phill | Phill@swift.com | True | 
| Jon | Jon@swift.com | False |


# Build Instructions 

Use `docker-compose up -d` to run the container

Then use Adminer to setup your database tables and set all the permissions 
