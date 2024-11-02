# Cat Shelter Admin Portal

This project is a web application for managing cat adoptions for a shelter, built using Python, Flask, and MySQL. 
It allows (admin) users to add new cats, manage adoptions, and search for cats and adopters.

## Search Functionalities
Query by:
- Cat ID
- Cat Name
- Adopter ID
- Adopter Name
- Birthday (YYYY-MM-DD)
- Age Range (Kitten, Young, or Adult)

## Requirements
- Python
- Flask
- Flask-SQLAlchemy
- PyMySQL
- MySQL





## Initial Setup Instructions

### 1. Install the MySQL Database
- On macOS, you can use Homebrew to install MySQL: `brew install mysql`
- Start the MySQL server: `brew services start mysql`
- Secure the MySQL installation: `mysql_secure_installation`
- Create Database and User: `mysql -u root -p`

`CREATE DATABASE cat_shelter;`

`CREATE USER 'cat_user'@'localhost' IDENTIFIED BY 'password';`

`GRANT ALL PRIVILEGES ON cat_shelter.* TO 'cat_user'@'localhost';`

`FLUSH PRIVILEGES;`



### 2. Log in to MySQL and Set Up the Database
- Log in: `mysql -u root -p`
- Use the Database: `USE cat_shelter;`
- Exit the MySQL monitor: `quit` 

In the terminal, navigate to the directory containing the SQL files.
- Drop Existing Tables: `mysql -u root -p cat_shelter < drop_tables.sql`
- Create Tables: `mysql -u root -p cat_shelter < schema.sql`
- Insert Sample Data: `mysql -u root -p cat_shelter < insert_sample_data.sql`



### 3. Install the Required Python Packages
- In the terminal, navigate to the project root directory and run: `pip install Flask Flask-SQLAlchemy PyMySQL`


### 4. Run the Flask application
- In the project root directory, run: `python app.py`

The application will be accessible at http://127.0.0.1:5000/





## Running the app

### 1. Log in to MySQL and Set Up the Database
- Log in: `mysql -u root -p`
- Use the Database: `USE cat_shelter;`
- Exit the MySQL monitor: `quit` 

In the terminal, navigate to the directory containing the SQL files.
- Drop Existing Tables: `mysql -u root -p cat_shelter < drop_tables.sql`
- Create Tables: `mysql -u root -p cat_shelter < schema.sql`
- Insert Sample Data: `mysql -u root -p cat_shelter < insert_sample_data.sql`



### 2. Run the Flask Application
- In the project root directory, run: `python app.py`

The application will be accessible at http://127.0.0.1:5000/




## Tips for Running the App
- Ensure the MySQL server is running before starting the Flask application
- Replace 'cat_user' and 'password' with your actual MySQL user and password in the Flask application configuration
- The Flask development server will be accessible at http://127.0.0.1:5000/ by default