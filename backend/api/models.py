from django.db import models

class UserAuth(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, default='DefaultUsername')
    salt = models.CharField(max_length=32) 
    hashed_password = models.CharField(max_length=64) 
    email = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id
