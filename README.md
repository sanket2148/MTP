# TALK-Scribe

## Description
**Talk-Scirbe** is designed to facilitate text annotation on images using speech recognition technology. It streamlines the process of labeling image-based text data, which can be utilized in various machine learning and data processing workflows. The platform supports four distinct user roles, each with specialized access and capabilities:

### User Roles

**Talk-Scirbe** supports different user roles, each with distinct permissions and capabilities within the system.

- **Admin**: 
  - Responsible for overall system administration, user management, and high-level operations.
  - Capable of uploading images in various languages to be used for annotation tasks.
  - Selects annotators and validators for carrying out annotation and validation tasks, respectively.
  - Assigns specific images for annotation or validation to the chosen annotators or validators.
  - Monitors the progress of tasks and manages the distribution of work among users.
  - Ensures the integrity of the data and oversees the quality control process.

- **Researcher**: 
    - Focused on analyzing annotated data for research purposes. The researcher user can:
        - View all annotations and images of languages he is interested in.
        - Download annotations and images if they are not set as confidential by the admin.
        
- **Annotator**: 
    - An annotator can annotate images assigned by the admin using speech-to-text capabilities for multiple languages. An annotator can:
        - Annotate images assigned by the admin.

- **Validator**: 
    - Ensures the quality and accuracy of annotations by reviewing and validating the work done by annotators.

Each role is integral to the collaborative environment of Talk-Scirbe, ensuring efficient and accurate annotation of text images for enhanced data quality.

## Getting Started
To get started with Talk-scribe, please follow the installation and setup instructions outlined in this document. They will guide you through the process of setting up your local development environment, as well as the initial configuration of the application for first-time use.

### Dependencies
* Python 3.8 or higher
* Django 5.0.1
* See `requirements.txt` for a full list of dependencies

### Setting Up
* Clone the repository to your local machine
* Navigate to the project directory `cd myapp\myproject\newapp`
* Set up a virtual environment: `python -m venv venv` and activate it
* Install dependencies using `pip install -r requirements.txt`
* Create a copy of `settings.py` and update the variables as per your environment requirements, especially `SECRET_KEY`, `DEBUG`, and database configurations.

### Configuring Environment Variables
* Set environment variables for sensitive information like `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in `settings.py`.


## Features
* **Admin Interface**: Manage users and oversee the entire annotation process.
* **Researcher Tools**: Upload images for annotation and review submitted annotations.
* **Annotator Access**: Use speech recognition to annotate images with text.
* **Validator Functions**: Validate the annotations made by annotators for accuracy and quality.
 
# Directory Structure

Below is an outline of the key directories and files within this Django project, along with a description of their purpose:

- `myproject/`: The main project directory.
  - `settings.py`: Project settings/configuration.
  - `urls.py`: Project URL declarations for all applications included in the project.
  - `wsgi.py`: An entry-point for WSGI-compatible web servers to serve project.
  - `__init__.py`: Indicates that the directory should be treated as a Python package.

- `newapp/`: A Django application within the project, containing the core functionality.
  - `admin.py`: Configuration for the Django admin interface, defining how models are represented in the built-in Django Admin site.
  - `apps.py`: Configuration for the app itself, often including app-related settings.
  - `forms.py`: Definitions of Django Forms based on the models, which ease the creation of form-related HTML and validation.
  - `models.py`: Definitions of the database models which Django ORM translates into database tables.
  - `tests.py`: Test cases for the application to test  views, models, and other parts of the application.
  - `views.py`: Views for handling the business logic and rendering data to templates.
  - `signals.py`: Configuration of signals which are utilities that allow decoupled applications to get notified when actions occur elsewhere in the framework.
  - `urls.py`: URL declarations for this app specifically, including the "wiring" of views to URLs.
  

- `templates/`: Directory containing the app's templates, which are HTML files that allow for the separation of presentation and business logic.
    - `aaa.html`: HTML template for [describe purpose if applicable].
    - `add_remove.html`: HTML template for adding and removing the annotator for assigning the task/image to annotate.
    - `admin_home_page.html`: HTML template for home page or admin , where user will have a list of language folders containing images accordingly.
    - `annotator.html`: HTML template for the annotator home page user interface.
    - `api_settings.html`: Template for API settings interface.
    - `assign_task.html`: Template for assigning tasks to annotators whom the admin as selected in the add_remove.
    - `change_password_annotator.html`: Template for changing an annotator's password.
    - `change_password_researcher.html`: Template for changing a researcher's password.
    - `change_password.html`: Template for changing a user's password.
    <!-- - `check_annotation copy.html`: [Describe purpose if applicable]. -->
    - `check_annotation_annotator.html`: HTML template for annotators to checking the annotation done the annotator which he/she as done.
    - `check_annotation_researcher.html`: HTML template for researchers to checking the annotation of particular language images which the researcher is intrested and the image are not confidentital.
    - `check_annotation_validator.html`: HTML template for validators  to check and validate the annotations which are assigned by the admin.
    - `check_annotation.html`: HTML template for Admins to checking and validating the annotation whicha are done on the image he/she as uploaded.
    - `create_account.html`: HTML template for account creation.
    <!-- - `download_data_admin.html`: HTML template for [describe purpose if applicable].
    - `download_data_annotator.html`: HTML template for [describe purpose if applicable].
    - `download_data_researcher.html`: HTML template for [describe purpose if applicable]. 
    - `download_data.html`: HTML template for downloading data.-->
    - `help.html`: Help page template.
    - `language_folder_annotator.html`: HTML template for displaying different language folder content , cna check the images which are assigned for annotation.
    - `language_folder_researcher.html`: HTML template for displaying different language images.
    - `language_folder.html`: Template displaying different language images and has option to upload image , download images , mark images as confidential or non confidential.
    - `loginpage.html`: HTML template for user login.
    - `researcher.html`: HTML template for the researcher home page user interface.
    - `settings_annotator.html`: HTML template for annotators for changing the setting for the interface.
    - `settings_researcher.html`: HTML template for researchers  for changing the setting for the interface..
    - `settings_validator.html`: HTML template for validators for changing the setting for the interface..
    - `settings.html`: HTML template for admins for user settings.
    - `start_annotation_annotator.html`: HTML template for annotators to do the annotation.
    - `start_annotation.html`: HTML template for Admins to do the annotation.
    - `validator.html`: HTML template for the validator user interface.
    - `verify_otp.html`: HTML template shown after verification email is sent.To put the Otp and veirfy the email to create the account.
    - `welcomepage.html`: The welcome page template.


  - `static/`: Directory containing the app's static files, such as CSS, JavaScript, and images.
    - `css/`: Contains CSS files.
    - `js/`: Contains JavaScript files.
    - `images/`: Contains image files.

- `manage.py`: A command-line utility that lets you interact with this Django project in various ways.

- `requirements.txt`: A file listing the Python dependencies of the project.

- `README.md`: The file you’re currently reading that provides documentation for this project.


### Database Configuration

#### Overview
The database configuration in Django is managed through the `settings.py` file within the project directory. This file contains settings for various aspects of Talk-scribe , including database connection details.

#### Configuration
In the `settings.py` file, you'll find a section dedicated to configuring the database. Here's a breakdown of the key components:


**DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}**


### Database Setup
* Set up the database by running `python manage.py migrate`

### Static Files
* Collect static files using `python manage.py collectstatic` (if in production)

### Running the Project
* Start the development server with `python manage.py runserver`
* Access the application at `http://localhost:8000` in your web browser (for example : http://localhost:8000/newapp/create_account/)



## Help
If you encounter any issues, please refer to the Django documentation [here](https://docs.djangoproject.com/en/5.0/).

## Authors
Sanket D Avaralli -- Email -(mailto:sanketavaralli321@gmail.com)

## Version History
* 0.1 - Initial release

## License
Still need to be licensed.

## Acknowledgments
* Django Team for the comprehensive framework
* Dr. Narayanan (CK) C Krishnan , Associate Professor , Data Science
