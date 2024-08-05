from django.db import models

# Create your models here.
class Attempt(models.Model):
    email = models.EmailField(max_length=254, null=False)
    gate = models.IntegerField(default=0, null=False)
    start_time = models.DateTimeField(auto_now_add=True)
    curr_ans = models.TextField(default='seagull', max_length=255, null=False)
    expires = models.DateTimeField()
    
    
    
class Completion(models.Model):
    email = models.EmailField(max_length=254, null=False)
    total_time = models.DurationField() # set this with a timedelta
    gate = models.IntegerField(default=1, null=False)