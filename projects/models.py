from django.db import models
from clients.models import Client
from users.models import CustomUser

class Project(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    deadline = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Ongoing', 'Ongoing'), ('Completed', 'Completed')],
        default='Pending'
    )
    assigned_team = models.ManyToManyField(CustomUser, related_name='projects', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title