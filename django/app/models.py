from django.db import models
from datetime import datetime
        
class Contest(models.Model):

    contest_name = models.CharField(
        max_length=255,
    )
    
    start_date = models.DateTimeField(default=datetime.now(), blank=False)
    
    end_date = models.DateTimeField(default=datetime.now(), blank=False)
    
    hashtag_one = models.CharField(max_length=140)
    hashtag_one_typos = models.IntegerField(default = 0, blank=True)


    hashtag_two = models.CharField(max_length=140)
    hashtag_two_typos = models.IntegerField(default = 0, blank=True)

    finished = models.BooleanField(default=False, blank=False)

    winner = models.IntegerField(default=0, blank=False)

    def __str__(self):

        return self.contest_name
