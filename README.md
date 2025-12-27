# Internal Data Tool

This repository contains an internal data tool designed to facilitate data management and analysis within our organization. The tool provides a user-friendly interface for accessing, manipulating, and visualizing data from various sources.

## Features
 - App factory pattern (`app/__init__.py`)
 - Simple rooting system (`app/routes/some_route.py`)
 - Database integration using SQLAlchemy (`app/models.py`)

## Installation
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   export FLASK_APP=app:create_app  # On Windows use `set FLASK_APP=app:create_app`
   flask run --reload
   ```
   
## Project Layout
- `run.py`: Entry point to run the application.
- `app/`: Main application package.
  - `__init__.py`: Application factory.
  - `routes/`: Contains route definitions.
  - `models.py`: Database models using SQLAlchemy.
- `requirements.txt`: List of dependencies.


## Progress
- [x] Set up Flask application with app factory pattern.
- [x] Implement simple routing system.
- [x] Integrate SQLAlchemy for database management.
- [ ] Add user authentication.
- [ ] Implement data visualization features.
- [ ] Write unit tests for the application.
- [ ] Create documentation for end-users.
- [ ] Deploy the application to a production environment.
