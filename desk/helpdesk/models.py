from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

STATUS_CHOICES = (
    ('new', 'New'),
    ('in_progress', 'In Progress'),
    ('resolved', 'Resolved'),
    ('confirmed', 'Confirmed'),
)



class HellpDesk(models.Model):
    name = models.CharField(max_length=50) # asker
    phone = models.IntegerField()
    email = models.CharField(max_length=255)
    description = models.TextField()
    creator_name = models.CharField(max_length=255, default='idontknow')
    CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    ]
    priority = models.CharField(max_length=100, choices=CHOICES)
    status = models.CharField(max_length=250, choices= STATUS_CHOICES , default="new")
    date = models.DateField(default=timezone.now)
    actions_taken = models.TextField(blank=True)
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL , null= True , related_name='assigned_problem_more')
    resolved_user = models.ForeignKey(User, on_delete=models.SET_NULL , null= True , related_name = 'resolved_problem_more' )
    confirmed = models.BooleanField(default=False)

    def str(self):
        return self.name
    

