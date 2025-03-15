from django.db import models

class UserAuth(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    salt = models.CharField(max_length=32)  # storing hex representation (16 bytes => 32 hex characters)
    hashed_password = models.CharField(max_length=64)  # SHA256 hash in hex (64 characters)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id
