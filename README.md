# AdCreative Project

AdCreative is a Django-based web application that provides an interface for generating images and advertisements. The application allows users to upload images, process them, and generate advertisements based on templates.

## Technologies Used

- **Python:** The primary programming language used for developing the application.
- **Django:** A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **SQLite:** The default database used by Django for storing data.
- **Django Admin:** A built-in module of Django for administrative activities.

## Key Features

- **Image Generation:** Users can upload an image which is then processed and stored. The processed image can be viewed in the Django admin interface.
- **Advertisement Generation:** Users can create an advertisement template which includes a logo, punchline, button text, and color scheme. The generated advertisement can be viewed in the Django admin interface.

## Directory Structure

- `adcreative`: This is the main Django project directory. It contains the settings and URL configuration for the project.
- `imageapi`: This is a Django app within the project. It contains the models for `ImageGeneration` and `AdvertisementTemplate`, the admin configuration for these models, and the views for processing images and generating advertisements.
- `migrations`: This directory contains Django migration files for applying changes to the database schema.

## Setup and Running the Project

Before running the project, make sure you have Python and Django installed on your system. Then, navigate to the project directory and run the following command to start the Django development server:

```sh
python manage.py runserver
```

The server will start on http://127.0.0.1:8000/. You can access the Django admin interface at http://127.0.0.1:8000/admin/.
