# SyncMore

## Overview
SyncMore is a web application developed as part of The HomeMore Project, designed to provide cloud storage services and centralized resources for unhoused individuals in California. It allows users to store and digitize important personal documents and access a collection of resources aimed at supporting their journey towards securing permanent housing.

## Getting Started

### Prerequisites
- Python [specify version]
- Django [specify version]
- Other dependencies (list other major libraries or tools required)

### Installation
1. Clone the repository:

    `git clone git@github.com:mzkahane/SyncMore.git`

2. Navigate to the project directory:

    `cd SyncMore`

3. Install required dependencies:

    `pip install -r requirements.txt`

### Building the Application
To build SyncMore, follow these steps:
1. Initialize the database (if using a database):

    `python manage.py makemigrations`

    `python manage.py migrate`

2. Collect static files (if applicable):

    `python manage.py collectstatic`

## Running the Application
Run the application using the Django development server:

    python manage.py runserver

Access the application at `http://localhost:8000` in your web browser.

## Running Tests
Execute the following command to run the tests:

    python manage.py test

This will run all the test cases defined in the application.

## What to Expect
When you run SyncMore, you can expect the following features to be available:
- User authentication system: Log in and manage user accounts.
- Cloud storage functionality: Upload, store, and manage personal documents.
- Resource directory: Access a curated list of resources for unhoused individuals.

## Contributing
Contributions to SyncMore are welcome. Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests.

## License
This project is licensed under the [specify license] - see the `LICENSE.md` file for details.

## Acknowledgments
- Mention any contributors, third-party libraries, or other resources used in the project.


[//]: # (To run the project SyncMore on any local PC, you will need some dependencies, please use the commands below to install:)

[//]: # (   )
[//]: # (     pip install Django)

[//]: # (To run the project SyncMore, please navigate to the root directory, run:)

[//]: # ()
[//]: # (    python3 manage.py runserver)

[//]: # ()
[//]: # (For object storage, please install the following package:)

[//]: # ()
[//]: # (    pip install django-storages boto3)

[//]: # (    )
[//]: # (    pip install requests)