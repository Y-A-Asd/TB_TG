Installation
============

To install the Django Online Shop TB_TG, follow these steps:

1. **Clone the Repository**:
   
   Start by cloning the repository to your local machine:

   ::

       git clone https://github.com/Y-A-Asd/TB_TG.git

2. **Create a Virtual Environment**:

   It's recommended to use a virtual environment to manage dependencies. Create a virtual environment using your preferred tool (e.g., virtualenv or venv):

   ::

       virtualenv env

   Activate the virtual environment:

   - On Windows:

     ::

         env\Scripts\activate

   - On Unix or MacOS:

     ::

         source env/bin/activate

3. **Install Dependencies**:

   Navigate to the project directory and install the required dependencies using pip:

   ::

       cd django-online-shop-tb_tg
       pip install -r requirements.txt

4. **Set Up Redis**:

   If you haven't already, install Redis on your system. You can download and install Redis from the official website: `Redis Download <https://redis.io/download>`_.

5. **Run Redis Server**:

   Start the Redis server on your local machine. You can do this by running the following command in a terminal or command prompt:

   ::

       redis-server

6. **Database Setup**:

   Set up your database configuration in the settings file (e.g., settings.py) and apply migrations:

   ::

       python manage.py migrate

7. **Start Celery Worker**:

   Run the Celery worker to handle background tasks. Open a new terminal or command prompt, activate the virtual environment, navigate to the project directory, and run the following command:

   ::

       celery -A TB_TG worker -l info

8. **Create Superuser**:

   Create a superuser account to access the admin panel:

   ::

       python manage.py createsuperuser

9. **Run the Development Server**:

   Start the development server to run the Django Online Shop TB_TG locally:

   ::

       python manage.py runserver

10. **Access the Application**:

    Open your web browser and navigate to the following URL to access the Django Online Shop TB_TG:

    ::
    
        http://localhost:8000

    You can also access the admin panel by appending "/admin" to the URL and logging in with the superuser credentials created in step 8.