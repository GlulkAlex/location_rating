# Description:  

What Is This All About ?  

## Test assignment (1-2 hours estimate): ##
Implement a Lambda function   
in a standalone Python module that:  
* Takes geo coordinates (lat/long)  
  and 'restaurant name'  
  as params  
* Returns Yelp or TripAdviser ( choose one ) 'rating of the location'  
* Prints out  
  and stores the result  
  in any PostgresDB  

### Use: ###  
* [Python 3.6 runtime](https://docs.python.org/3.6/whatsnew/3.6.html)  
* [PostgresDB](https://www.postgresql.org/)  
* [Yelp](https://www.yelp.com/developers/graphql/guides/intro)  
* [TripAdviser](https://www.tripadvisor.com)  

The code must be highly comprehensible 
and must have a logical structure .  
( It might have unit tests  
  with coverage report . )  

Tests might be done with [pytest](https://docs.pytest.org/en/latest/contents.html),  
or [unittest package](https://docs.python.org/3/library/unittest.html#module-unittest).  
Coverage might be done with [coverage package](https://coverage.readthedocs.io)  
or [pytest-cov](http://pytest-cov.readthedocs.io/en/latest/) for [pytest](https://docs.pytest.org/en/latest/contents.html).  

---

Use cases:  
===
* Takes geo coordinates (lat/long) and restaurant name as params  
* Returns Yelp or TripAdviser ( choose one ) rating of the location  
* Prints out and stores the result in any PostgresDB  

## How to install:  

In order to  
automatically create  
and manage a `virtualenv` for the project,  
as well as add packages from the `Pipfile`  
start by [Installing Pipenv](https://docs.pipenv.org/#install-pipenv-today) .

1. Clone / create project repository from public repo:  
   `$ ? clone https://?`      
2. Then withing `$ cd <my_project>`  
   Install from Pipfile:  
   `$ pipenv install`  

PostgreSQL  
is available  
in all Ubuntu versions  
[by default](https://www.postgresql.org/download/linux/ubuntu/).  
[PostgreSQL install procedure](https://www.postgresql.org/docs/10/static/install-procedure.html)  
[Psycopg](http://initd.org/psycopg/docs/install.html#build-prerequisites)  
for example,   
To install PostgreSQL on Ubuntu,  
use the apt-get (or other apt-driving) command:  
`$ apt-get install postgresql-10`  
[PostgreSQL Installation](https://help.ubuntu.com/stable/serverguide/postgresql.html)  
[install PostgreSQL via the apt package manager](https://www.fullstackpython.com/blog/postgresql-python-3-psycopg2-ubuntu-1604.html)  
`$ createdb test_db`  
or:  
`postgres=# CREATE DATABASE test_db;`  

---

## How to run:  

In order to  
start the application .  

1. Activate the Pipenv shell:  
   `$ pipenv shell`  
   to spawn environment shell (/bin/bash).  
   Use 'exit' to leave.  
2. Next, start the ? main script ? ( application entry point )  
   from `src/?/`:   
   `$ python location_rating.py`  
   or from the project root directory:  
   `$ src/?/location_rating.py`  
   Press Ctrl-C (or Ctrl-Break on Windows)  
   to stop the application.  

`$ sudo apt-get install postgresql-9.6`  
Success. You can now start the database server using:  

    /usr/lib/postgresql/9.6/bin/pg_ctl -D /var/lib/postgresql/9.6/main -l logfile start  

Ver Cluster Port Status Owner    Data directory               Log file  
9.6 main    5434 down   postgres /var/lib/postgresql/9.6/main /var/log/postgresql/postgresql-9.6-main.log  

list all the postgres clusters running:  
`$ pg_lsclusters`  
Ver Cluster Port Status Owner    Data directory               Log file  
9.4 main    5432 down   postgres /var/lib/postgresql/9.4/main /var/log/postgresql/postgresql-9.4-main.log  
9.5 main    5433 down   postgres /var/lib/postgresql/9.5/main /var/log/postgresql/postgresql-9.5-main.log  
9.6 main    5434 down   postgres /var/lib/postgresql/9.6/main /var/log/postgresql/postgresql-9.6-main.log  

to look into PostgreSQL Client Authentication Configuration File:  
`$ sudo cat /etc/postgresql/<version e.g.: 9.6>/main/pg_hba.conf`  

[Starting the Database Server](https://www.postgresql.org/docs/9.6/static/server-start.html)  
the server must be run  
by the PostgreSQL user account  
and not by root  
or any other user.  
Therefore  
you probably should form your commands using `su postgres -c '...'`.  
For example:  
`$ su postgres -c 'pg_ctl start -D /usr/local/pgsql/data -l serverlog'`  

$ sudo -u postgres /usr/lib/postgresql/9.6/bin/pg_ctl -D /var/lib/postgresql/9.6/main -l logfile start  
server starting  
/bin/sh: 1: cannot create logfile: Permission denied  

`$ sudo /usr/lib/postgresql/9.6/bin/pg_ctl -D /var/lib/postgresql/9.6/main -l logfile start`  
pg_ctl: cannot be run as root  
Please log in (using, e.g., "su") as the (unprivileged) user that will  
own the server process.  

`$ su postgres -c "/usr/lib/postgresql/9.6/bin/pg_ctl -D /var/lib/postgresql/9.6/main -l logfile start"`
and
`$ sudo su -c "/usr/lib/postgresql/9.6/bin/pg_ctl -D /var/lib/postgresql/9.6/main -l logfile start" <user>`
pg_ctl: could not open PID file "/var/lib/postgresql/9.6/main/postmaster.pid": Permission denied

so ( in my case ) just run:  
`$ sudo systemctl start postgresql`  
or:  
`$ sudo systemctl restart postgresql.service`  
or same but [with restart](https://www.tutorialspoint.com/postgresql/postgresql_environment.htm):  
`$ service postgresql restart`  
or:  
`$ sudo service postgresql restart`  
this also works:  
`$ <sudo> service postgresql start`  
and then  
to start [PostgreSQL interactive terminal](https://www.postgresql.org/docs/current/static/app-psql.html):  
`$ psql`  
inside shell:  
`<user>=# \?`  
List of databases:  
`<user>=# \l+`  
List of relations:  
`<user>=# \dt+`

---

## How to Test:  

to discover all available tests from parent | root folder:  
`$ python -m unittest discover`  

If `py.test` is installed:  
`$ py.test -q`  
To run | execute specific test only:  
`$ py.test tests/test__location_rating.py`  

If installed the `pytest-cov` package,    
we can run the tests with coverage .  
( Note: this could produce lots of unrelated info e.g. about libs )  
`$ py.test --cov --cov-report=term-missing`  
or ( but still not very specific )   
`$ py.test --cov --cov-report=term-missing src/?/db_explorer_main.py`   

Configuration defaults for `py.test` and test coverage.  
These configuration files are  
`pytest.ini` and `.coveragerc`,  
located at the root of your package.  
Without these defaults,  
we would need to specify  
the path to the module  
on which we want to run tests and coverage.  
`$ py.test --cov=tests tests/test_functional.py -q`  

Use `$ coverage run db_explorer_main.py`  
to run your program and gather data .  
`$ coverage run --source=. src/db_explorer/db_explorer_main.py`  
Note: it raises   
`NotImplementedError: Can't perform this operation for unregistered loader type`  
for ? Mako templates ?   

Coverage summary:  
`$ coverage report`  
The -m flag shows the line numbers of missing statements:  
`$ coverage report -m`  

Make annotated copies of the given files,  
marking statements  
that are executed with `>`  
and statements that are missed with `!`.  
`$ coverage annotate --directory=reports db_explorer_main.py`  

---
