from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_userauth_name'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE TABLE myapp_userauth (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL UNIQUE,
                    name VARCHAR(255) NOT NULL DEFAULT 'DefaultUsername',
                    salt VARCHAR(32) NOT NULL,
                    hashed_password VARCHAR(64) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """,
            reverse_sql="DROP TABLE myapp_userauth;"
        )
    ]
