# Cafe Management API

The Cafe Management API is a Flask-based web application that allows you to manage information about cafes, including their location, facilities, and coffee prices.
You can use this API to add new cafes, update cafe prices, report cafes as closed, and retrieve cafe data based on various criteria. 
The data is stored in a database, and the application provides both HTML views and JSON responses for various operations.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python: Make sure you have Python 3.x installed.
- Dependencies: Install the required dependencies using `pip`:
- Database: Set up a database and provide its connection string as an environment variable named `DATABASE`.
- API Key: Generate an API key and store it as an environment variable named `API_KEY`.

## API Endpoints
- /: Homepage, provides an HTML view.
- /random: Returns information about a randomly selected cafe in JSON format.
- /all: Returns information about all cafes in the database in JSON format.
- /search?loc=location: Returns cafes at a specific location (replace location with the desired location).
- /add?api-key=yourapikey (POST): Add a new cafe to the database (requires the correct API key).
- /update-price/<cafe_id>?new_price=newprice (GET or PATCH): Update the coffee price of a cafe by its ID.
- /report-closed/<cafe_id>?api-key=yourapikey (GET or DELETE): Mark a cafe as closed and remove it from the database (requires the correct API key).

You can see the documentation in the link: https://documenter.getpostman.com/view/30329575/2s9YR9YCt6
