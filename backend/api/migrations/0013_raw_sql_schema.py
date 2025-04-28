from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_maintenancerequest_status'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                -- Table for UserAuth
                CREATE TABLE IF NOT EXISTS userauth (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL UNIQUE,
                    name VARCHAR(255) NOT NULL DEFAULT 'DefaultUsername',
                    salt VARCHAR(32) NOT NULL,
                    hashed_password VARCHAR(64) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    is_admin BOOLEAN NOT NULL DEFAULT FALSE
                );

                -- Table for Student
                CREATE TABLE IF NOT EXISTS student (
                    student_id INTEGER PRIMARY KEY,
                    name VARCHAR(255) NOT NULL DEFAULT 'DefaultUsername',
                    email VARCHAR(255) NOT NULL UNIQUE,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER NOT NULL UNIQUE,
                    CONSTRAINT fk_student_user
                        FOREIGN KEY (user_id)
                        REFERENCES userauth(id)
                        ON DELETE CASCADE
                );

                -- Table for Dorm
                CREATE TABLE IF NOT EXISTS dorm (
                    dorm_id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    address VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                -- Table for Room
                CREATE TABLE IF NOT EXISTS room (
                    room_id SERIAL PRIMARY KEY,
                    room_number VARCHAR(50) NOT NULL,
                    capacity INTEGER NOT NULL DEFAULT 1,
                    is_available BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    has_ac BOOLEAN NOT NULL DEFAULT FALSE,
                    has_private_bath BOOLEAN NOT NULL DEFAULT FALSE,
                    cost_per_month DECIMAL(6,2) NOT NULL DEFAULT 0.00,
                    current_occupants INTEGER NOT NULL DEFAULT 0,
                    dorm_id INTEGER NOT NULL,
                    CONSTRAINT fk_room_dorm
                        FOREIGN KEY (dorm_id)
                        REFERENCES dorm(dorm_id)
                        ON DELETE CASCADE
                );

                -- Table for studentBooking
                CREATE TABLE IF NOT EXISTS studentbooking (
                    booking_id SERIAL PRIMARY KEY,
                    booking_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    lease_length INTEGER NOT NULL,
                    dorm_name VARCHAR(255) NOT NULL,
                    room_number VARCHAR(50) NOT NULL,
                    student_id INTEGER NOT NULL,
                    confirmed BOOLEAN NULL DEFAULT NULL,
                    status BOOLEAN NULL DEFAULT NULL,
                    CONSTRAINT fk_booking_student
                        FOREIGN KEY (student_id)
                        REFERENCES userauth(id)
                        ON DELETE CASCADE
                );

                -- Table for StudentInfo
                CREATE TABLE IF NOT EXISTS student_info (
                    id BIGSERIAL PRIMARY KEY,
                    phone_number VARCHAR(20),
                    home_address VARCHAR(255),
                    emergency_contact VARCHAR(255),
                    user_id INTEGER NOT NULL UNIQUE,
                    CONSTRAINT fk_studentinfo_user
                        FOREIGN KEY (user_id)
                        REFERENCES userauth(id)
                        ON DELETE CASCADE
                );

                -- Table for MaintenanceRequest
                CREATE TABLE IF NOT EXISTS maintenancerequest (
                    request_id SERIAL PRIMARY KEY,
                    student_id VARCHAR(25) NOT NULL,
                    issue VARCHAR(2000) NOT NULL,
                    location VARCHAR(1000) NOT NULL,
                    priority VARCHAR(50) NOT NULL,
                    date_created VARCHAR(50) NOT NULL,
                    status BOOLEAN NULL DEFAULT NULL
                );
            """,
            reverse_sql="""
                DROP TABLE IF EXISTS maintenancerequest;
                DROP TABLE IF EXISTS student_info;
                DROP TABLE IF EXISTS studentbooking;
                DROP TABLE IF EXISTS room;
                DROP TABLE IF EXISTS dorm;
                DROP TABLE IF EXISTS student;
                DROP TABLE IF EXISTS userauth;
            """
        )
    ]
