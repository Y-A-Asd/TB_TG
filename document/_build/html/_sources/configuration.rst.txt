Configuration
=============

The Django Online Shop TB_TG project offers various configuration options that users can customize to tailor the project to their specific needs. Below are some of the key configuration settings:

1. **Database Configuration**:
   
   - **Database Engine**: Configure the database engine (e.g., SQLite, PostgreSQL, MySQL).
   - **Database Name**: Specify the name of the database.
   - **Database User and Password**: Provide credentials for accessing the database.
   - **Database Host and Port**: Optionally specify the host and port if using a remote database server.

2. **Django Settings**:

   - **SECRET_KEY**: Set a unique secret key for cryptographic signing.
   - **DEBUG**: Enable or disable debug mode for development or production environments.
   - **ALLOWED_HOSTS**: Define a list of allowed hosts for the Django project.
   - **STATIC_URL** and **STATIC_ROOT**: Configure settings related to serving static files.
   - **MEDIA_URL** and **MEDIA_ROOT**: Define settings for serving media files uploaded by users.
   - **TEMPLATES**: Customize template settings, including template directories, loaders, and context processors.
   - **AUTH_USER_MODEL**: Specify a custom user model if needed.

3. **Third-Party Integration**:

   - **Zarinpal Configuration**: If using the Zarinpal payment gateway, configure API keys or other authentication settings.
   - **Celery Configuration**: Customize Celery settings for background task processing, including broker URL and concurrency options.
   - **Redis Configuration**: Configure Redis settings for Celery task queue management and caching.

4. **Email Settings**:

   - **EMAIL_BACKEND**: Choose an email backend for sending emails (e.g., SMTP, console backend for development).
   - **EMAIL_HOST**, **EMAIL_PORT**, **EMAIL_HOST_USER**, **EMAIL_HOST_PASSWORD**: Specify SMTP server details if using SMTP backend.

5. **Logging Configuration**:

   - **LOGGING**: Customize logging settings for different loggers, handlers, and log levels.

6. **Custom Settings**:

   - Define any custom settings specific to your Django project or application.

7. **Dynamic Site Information (Admin)**:

   - **Site Settings**: Use the `SiteSettings` model to dynamically set site information such as footer text, address, phone number, logo, and social media links.
   - **Home Banner**: Utilize the `HomeBanner` model to manage home page banners and link them to specific products.

Users can modify these settings and models in the project's settings.py and models.py files, respectively, according to their requirements. It's important to review and update these settings and models carefully, especially in production environments, to ensure the proper functioning and customization of the Django project.
