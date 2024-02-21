# Backend readme

## Starting the application

We may use 'sudo bash run.sh build {containers_name}'

Once finished compiling:

Use 'sudo bash run.sh start' to launch the app.
We can check backend is working by accesing 'localhost:5000'

We can read data from defined variables in 'localhost:5000/read_data'

## Database

PostgreSQL DB is created when building the application. We can access databse via adminer in 'localhost:8085'
Credentials:
    - POSTGRES_USER= root
    - POSTGRES_PASSWORD= root
    - POSTGRES_DB= satc_database