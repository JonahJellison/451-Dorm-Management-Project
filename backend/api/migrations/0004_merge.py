
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_userauth_name'),
        ('api', '0003_create_all_tables_raw_sql'),
    ]

    operations = [
        # No operations are needed here. This migration just serves to merge the branches.
    ]
