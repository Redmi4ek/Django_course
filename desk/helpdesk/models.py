from django.db import models
from django.utils import timezone

# Create your models here.
class HellpDesk(models.Model):
    name = models.CharField(max_length=50) # asker
    phone = models.IntegerField()
    email = models.CharField(max_length=255)
    description = models.TextField()
    CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    ]
    priority = models.CharField(max_length=100, choices=CHOICES)
    status = models.CharField(max_length=250, default="new")
    date = models.DateField(default=timezone.now)
    actions_taken = models.TextField(blank=True)

    def str(self):
        return self.name
    

