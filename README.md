# TressTime

## Description
A platform for local businesses (Currently tailored to hairdressers but can be modified for other local businesses, eg: consultancies, fitness studios) to manage appointments and bookings.

## Key Features:
  - User authentication and role-based access control.
  - Calendar integration for viewing and managing bookings.
  - Automated email or SMS reminders.
  - Payment gateway integration for prepayments or deposits.

## Tech Stack:
  - **Backend**: 
    - Language: Python
    - Framework: Django
  - **Frontend**: 
    - Language: Javascript
    - Framework: React
    - State Management: Redux / Context API _(TODO: decide which to use)_
  - **Database Management**: PostgreSQL

## Design Patterns:
- **Repository Pattern**:
    - **Overview**: Mediates between the domain and data mapping layers, acting like an in-memory domain object collection.
    - **Utility**: Provides a cleaner way to access data from the database, making it easier to switch databases or data sources without affecting other parts of the application.
- **Service Layer**:
    - **Overview**: Provides a set of services available to the client, abstracting business logic from user interface and data access logic.
    - **Utility**: Enhances application's maintainability by consolidating business logic in one place, making it reusable and easier to modify.
- The Repository and Service Layer are complimentary patterns so they are both being used in this application

## Getting Started
_**NOTE:** This guide is for macOS environments_

Install the package manager Homebrew if you do not have it already (instructions can be found [here](https://brew.sh/)).

### Installing python requirements

**Installing python**

You can manage your python environments using pyenv (Or the tool of your choice)
```commandline
brew update
brew install pyenv
```
Add the following to your shell configuration file (.bashrc, .zshrc, etc.):
```
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"
```
Source your profile file to apply the changes:
```
source ~/.bash_profile  # If you are using bash
source ~/.zshrc          # If you are using zsh
```
Install the python file defined in the `.python-version` file:
```
pyenv install {python-version}
```

**Virtual environment**

You can set up your virtual environment using `virtualenv` (Or the tool of your choice). 
In the root directory of the project, simply run:
``` commandline
brew install virtualenv
virtualenv venv
```
This will install [virtualenv](https://virtualenv.pypa.io/en/latest/) and create a virtual environment called `venv`.

Next we will use pip to install the python packages. pip should have been automatically installed when creating the 
virtual environment in the previous step. Confirm this by running:

`pip --version`

If you have issues visit the [pip documentation page](https://pip.pypa.io/en/stable/installation/).

Install the python requirements for this project: `pip install -r requirements.txt`

### Setting up the database
The database manager used in this project is PostgreSQL. You will need to have it installed and running:  
```commandline
brew install postgresql
brew services start postgresql
```

Run the database setup script (you will be prompted to create a username and password; make a note of these, they will 
be reused in the next step): 

`./setup_db.sh`

### Credentials

This project uses `python-decouple` to manage credentials. By using an environment variable management library, we can 
effectively separate the configuration and sensitive credentials from the codebase, enhancing both security and 
flexibility of the project.

Create an `.env` file in the `django_app` directory and add the necessary environment variables:
```
DB_NAME='tresstime_db'
DB_USER={username_you_used_in__setup_db}
DB_PASSWORD={password_you_used_in__setup_db}
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY={see_below_for_generating_a_secret_key}
DEBUG=True
```
`DEBUG` should only be set to `True` in development/test environment and `False` in production.

**Generating a secret key**:
You can use Django’s built-in utility get_random_secret_key() to generate a new secret key. In the python shell, run:
```python
from django.core.management.utils import get_random_secret_key

new_secret_key = get_random_secret_key()
print(new_secret_key)
```

### Frontend

**Node Version Manager**  
This project uses Node Version Manager (NVM) to manage node versions. Install nvm, replacing the variable with the latest version:

`curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/{most_recent_stable_nvm}/install.sh | bash`

The most recent stable nvm version can be found [here](https://github.com/nvm-sh/nvm).

The above script clones the NVM repository from GitHub to ~/.nvm and adds the source line to your profile 
(~/.bash_profile, ~/.zshrc, ~/.profile, or ~/.bashrc)

Source your profile file to apply the changes:
```commandline
source ~/.bash_profile  # If you are using bash
source ~/.zshrc          # If you are using zsh
```
This command loads the nvm script into your session, enabling you to use nvm commands.

To confirm that nvm has been installed correctly, use:  
```
nvm --version
```
This command should return the version of nvm that you have installed.

**Node**  
Once nvm is installed, you can install Node.js. To install a specific version of Node.js, use:  
```commandline
nvm install {project_version_number}
```
The `project_version_number` can be found in the `.nvmrc` file in the root of the project.   
Next run:  
```
nvm use {project_version_number}
```
Ensuring that the returned version matches that defined in the `.nvmrc` file. Node should now be ready to use for
this project.

**Frontend build**

The frontend needs to be compiled. From the root of the project:

```commandline
cd react_app
npm run build
```

_**NOTE:** The build script has been modified so that the folder is moved into the relevant directory in `django_app`._

### Final steps and running the server locally

Run migrations, collect static assets and run the server. From the root of the project: 
```
cd django_app &&
python manage.py makemigrations &&
python manage.py collectstatic &&
python manage.py runserver
```

Visiting local host should display the homepage.
