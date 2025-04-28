# 451-Dorm-Management-Project

Running the app:

1. ensure that postgress is installed
If Not { 
    install from "https://www.postgresql.org/download/"
    Then check "C:\Program Files\PostgreSQL\17\data\postgresql.conf" has host set to 'localhost' and port is '5432'
}

2. Create database via terminal {
    > psql -U postgres
    > CREATE DATABASE mydatabase;
    > CREATE USER myuser WITH PASSWORD 'mypassword';
    > GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
}

3. Create virtual enviorment with all dependencies from requirements.txt

4. Run "npm install" 

5. Update settings.py to match psql user created {
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'mydatabase',
            'USER': 'myuser',
            'PASSWORD': 'mypassword',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
}

4. Apply Migrations and create superuser from terminal {
    451-Dorm-Managment-Project/backend> python manage.py migrate
    451-Dorm-Managment-Project/backend> python manage.py createsuperuser
}

5. Run the psql server from terminal {
    451-Dorm-Managment-Project/backend> python manage.py runserver
}

6. Populate the database with mock data from terminal {
    451-Dorm-Managment-Project/backend/api> python data_generator.py
}

7. Run the frontend from terminal {
    451-Dorm-Managment-Project/app-frontend> npm start 
}
