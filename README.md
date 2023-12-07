# SyncMore

[![My Skills](https://skillicons.dev/icons?i=js,html,css,bootstrap,jquery,python,django,mysql,cloudflare,figma,docker)](https://skillicons.dev)


[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![asgiref](https://img.shields.io/badge/asgiref-3.7.2-brightgreen)](https://pypi.org/project/asgiref/)
[![backports.zoneinfo](https://img.shields.io/badge/backports.zoneinfo-0.2.1-brightgreen)](https://pypi.org/project/backports.zoneinfo/)
[![boto3](https://img.shields.io/badge/boto3-1.33.7-brightgreen)](https://pypi.org/project/boto3/)
[![botocore](https://img.shields.io/badge/botocore-1.33.7-brightgreen)](https://pypi.org/project/botocore/)
[![certifi](https://img.shields.io/badge/certifi-2023.11.17-brightgreen)](https://pypi.org/project/certifi/)
[![Django](https://img.shields.io/badge/Django-4.2.8-brightgreen)](https://pypi.org/project/Django/)
[![idna](https://img.shields.io/badge/idna-3.6-brightgreen)](https://pypi.org/project/idna/)
[![jmespath](https://img.shields.io/badge/jmespath-1.0.1-brightgreen)](https://pypi.org/project/jmespath/)
[![PyMySQL](https://img.shields.io/badge/PyMySQL-1.1.0-brightgreen)](https://pypi.org/project/PyMySQL/)
[![requests](https://img.shields.io/badge/requests-2.31.0-brightgreen)](https://pypi.org/project/requests/)
[![s3transfer](https://img.shields.io/badge/s3transfer-0.8.2-brightgreen)](https://pypi.org/project/s3transfer/)
[![six](https://img.shields.io/badge/six-1.16.0-brightgreen)](https://pypi.org/project/six/)
[![sqlparse](https://img.shields.io/badge/sqlparse-0.4.4-brightgreen)](https://pypi.org/project/sqlparse/)
[![typing_extensions](https://img.shields.io/badge/typing_extensions-4.8.0-brightgreen)](https://pypi.org/project/typing_extensions/)
[![urllib3](https://img.shields.io/badge/urllib3-1.26.18-brightgreen)](https://pypi.org/project/urllib3/)
[![whitenoise](https://img.shields.io/badge/whitenoise-6.6.0-brightgreen)](https://pypi.org/project/whitenoise/)

## Overview

SyncMore is a web application developed as part of The [HomeMore](https://thehomemoreproject.org) Project, designed to
provide cloud storage services and centralized resources for unhoused individuals in California. It allows users to
store and digitize important personal documents and access a collection of resources aimed at supporting their journey
towards securing permanent housing.

## Getting Started

### Prerequisites

- asgiref 3.7.2
- backports.zoneinfo 0.2.1
- boto3 1.33.7
- botocore 1.33.7
- certifi 2023.11.17
- charset-normalizer 3.3.2
- Django 4.2.8
- django-storages 1.14.2
- idna 3.6
- jmespath 1.0.1
- PyMySQL 1.1.0
- python-dateutil 2.8.2
- requests 2.31.0
- s3transfer 0.8.2
- six 1.16.0
- sqlparse 0.4.4
- typing_extensions 4.8.0
- urllib3 1.26.18
- whitenoise 6.6.0

### Installation

1. Clone the Repository:

   `$ git clone git@github.com:mzkahane/SyncMore.git`

   or

   `$ git clone https://github.com/mzkahane/SyncMore.git`


2. Navigate to the Project Directory:

   `$ cd SyncMore`


3. Install Required Dependencies:

   `$ pip install -r requirements.txt`

### Setup the MySQL Database

1. Run this command in your database host:

   `$ sudo apt-get install mysql-server`


2. Set up the database detailed information in setting.py under the project folder.

### Setup the Email SMTP Service

1. Set up the Email SMTP detailed information in setting.py under the project folder.

### Setup the Object Storage Service

1. Set up the Object Storage detailed information in setting.py under the project folder.

### Building the Application

To build SyncMore, follow these steps:

1. Initialize the Database:

   `$ python manage.py makemigrations`

   `$ python manage.py migrate`


2. Collect Static Files:

   `$ python manage.py collectstatic`

## Running the Application

Run the application using the Django development server:

    $ python manage.py runserver

Access the application at `http://localhost:8000` in your web browser.

## Running Tests

Execute the following command to run the tests:

    $ python manage.py test

This will run all the test cases defined in the application.

## What to Expect

When you run SyncMore, you can expect the following features to be available:

- User authentication system: Log in and manage user accounts.
- Cloud storage functionality: Upload, store, and manage personal documents and notes.
- Resource directory: Access a curated list of resources for unhoused individuals.

## Running Server Deployment

1. Clone the Repository:

   `$ git clone git@github.com:mzkahane/SyncMore.git`

   or

   `$git clone https://github.com/mzkahane/SyncMore.git`


2. Navigate to the Project Directory:

   `$ cd SyncMore`


3. Install Required Dependencies:

   `$ pip install -r requirements.txt`


4. Collect Static Files:

   `$ python manage.py collectstatic`


5. Create uwsgi file:

   `vi uwsgi.ini`

   paste the content in the file:

   <code>[uwsgi] <br> socket=127.0.0.1:8000 <br> chdir=/root/SyncMore <br> wsgi-file=SyncMore/wsgi.py <br> process=4 <br> threads=2 <br> pidfile=uwsgi.pid <br> daemonize=uwsgi.log <br> master=true</code>


6. Enable uwsgi:

   `uwsgi --ini uwsgi.ini`


7. Edit nginx Configration:

   `sudo vim /etc/nginx/sites-enabled/default;`

   replace

   `try_files $uri $uri/ =404;`

   with

   <code>uwsgi_pass 127.0.0.1:8000; <br> include /etc/nginx/uwsgi_params;</code> 


8. Install nginx Service:

   `sudo apt install nginx`


9. Enable nginx Service:

   `sudo /etc/init.d/nginx start`

## Contributing

Contributions to SyncMore are welcome. Please contact [SyncMore team](https://syncmore.org/index/contact/) for details
on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the GNU General Public License - see
the [LICENSE](https://www.gnu.org/licenses/gpl-3.0.en.html) for details.

## Acknowledgments

- Contributors:
  [Andrew Liu](https://github.com/AndrewLiu666), [Vicki Young](https://github.com/tvyoung), [Matthew Kahane](https://github.com/mzkahane)
- Sponsor:
  [Zac Clark](zac@homemoreproject.org)
- Special Thanks: Jags Krishnamurthy, Saad Malik, Mingda Ma