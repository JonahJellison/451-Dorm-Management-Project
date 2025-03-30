from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        # Specify your previous migration, e.g., ('api', '0002_userauth_name'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                -- Table for UserAuth
                CREATE TABLE userauth (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL UNIQUE,
                    name VARCHAR(255) NOT NULL DEFAULT 'DefaultUsername',
                    salt VARCHAR(32) NOT NULL,
                    hashed_password VARCHAR(64) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );

                -- Table for Student
                CREATE TABLE student (
                    student_id INTEGER PRIMARY KEY,
                    name VARCHAR(255) NOT NULL DEFAULT 'DefaultUsername',
                    email VARCHAR(255) NOT NULL UNIQUE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );

                -- Table for studentBooking
                CREATE TABLE studentbooking (
                    booking_id SERIAL PRIMARY KEY,
                    student_id INTEGER NOT NULL,
                    booking_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    lease_length INTEGER NOT NULL,
                    CONSTRAINT fk_student
                        FOREIGN KEY (student_id)
                        REFERENCES student(student_id)
                        ON DELETE CASCADE
                );

                -- Table for Dorm
                CREATE TABLE dorm (
                    dorm_id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    address VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );

                -- Table for Room
                CREATE TABLE room (
                    room_id SERIAL PRIMARY KEY,
                    dorm_id INTEGER NOT NULL,
                    room_number VARCHAR(50) NOT NULL,
                    capacity INTEGER NOT NULL DEFAULT 1,
                    is_available BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT fk_dorm
                        FOREIGN KEY (dorm_id)
                        REFERENCES dorm(dorm_id)
                        ON DELETE CASCADE
                );
            """,
            reverse_sql="""
                DROP TABLE room;
                DROP TABLE dorm;
                DROP TABLE studentbooking;
                DROP TABLE student;
                DROP TABLE userauth;
            """
        )
    ]
