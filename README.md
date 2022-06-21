# SCL-2022-AMEYA

### Installation

1. - Fork the [repo](https://github.com/World-Konkani-Centre/SCL-2022-AMEYA)
   - Clone the repo to your local system
   ```git
   git clone https://github.com/World-Konkani-Centre/SCL-2022-AMEYA.git
   cd SCL-2022-AMEYA
   ```
   Make sure you have python installed on your system.
2. Create a Virtual Environment for the Project

   If u don't have a virtualenv installed

   ```bash
   pip install virtualenv
   ```

   ```bash
   virtualenv env

   source env/Scripts/activate
   ```

   If you are giving a different name than `env`, mention it in `.gitignore` first

3. Install all the requirements

   ```bash
   pip install -r requirements.txt
   ```

4. Make migrations/ Create db.sqlite3

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a super user.
   This is to access Admin panel and admin specific pages.

   ```djangotemplate
   python manage.py createsuperuser
   ```

   Enter your username, email and password.

6. Run server
   ```bash
   python manage.py runserver
   ```
