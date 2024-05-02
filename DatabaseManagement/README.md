# Environment
You need to have a `.env` file in the top level of the DatabaseManagement
directory. The minimal requirement for this file is two entries
```
HARNESS_DB_PASSWORD=<harness_db_password>
HARNESS_DB_USER=<user_name>
```
where `<harness_db_password>` is whatever password has been provided for 
your user name `<user_name>` to access the harness PostgreSQL database.