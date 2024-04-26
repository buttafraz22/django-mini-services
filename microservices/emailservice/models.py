from django.db import models

# Create your models here.

class Email(models.Model):
    content = models.TextField()
    sender_username = models.CharField(max_length=100)
    sent_to=models.EmailField()
    subject=models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(default='  ', max_length=2000) 

    def __str__(self):
        return f"Email from {self.sender_username} at {self.created_at}"
