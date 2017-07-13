from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import django
django.setup()

from django.core.management.base import BaseCommand, CommandError
from .models import Contest
from twitter import Twitter, OAuth
import enchant
import re
import json
from django.utils import timezone


dictionary = enchant.Dict("en_US")


#OAth keys
#Only have read permissions but still, be nice
CONSUMER_KEY = "5iY3qIL8De3DHFWeReCefAZKl"
CONSUMER_SECRET = "QJe9BHwQ0SKZ5jyTDrfGRYD4qO7WAPR74dMJ8LVO0nDcoNT6yv"
ACCESS_TOKEN = "339221168-Amag0DZPJqBrXO0ISdcyR5ZjbpNh9T7zp2G5hiSL"
ACCESS_SECRET = "B6riFQmrkZeOZHEU8so6eCDLkMRqfGL0rB2nAP8RuU6wr"

alphabetical = re.compile('[^a-zA-Z]')




# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'both.settings')

app = Celery('both')

# Pulls django configuration data and finds all tasks.  Although there's only one task.
#app.config_from_object('django.conf:settings')
#app.autodiscover_tasks(packages=None, related_name='tasks')


def count_typos(twitter_data):
    typos = 0

    for item in twitter_data["statuses"]:
        for word in item["text"].split(" "):
            #This removes all non-alphabetical characters from the string
            word = alphabetical.sub('', word)
            #Dictionary.check returns false in the case of a mispelling, so we're using that
            #The regex can strip this thing down to 0 characters in some cases, so we skip over that case 
            if word[0:4]!="http" and len(word)>0 and not dictionary.check(word.lower()):
                typos += 1
    return typos


@app.task(bind=True)
def update_contests(self):
    oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter = Twitter(auth=oauth)
    for contest in Contest.objects.filter(finished=False).filter(start_date__lte=timezone.now()):
        try:
            # Search for tweets from the first hashtag and process them
            hashtag_one_data = twitter.search.tweets(q="#"+contest.hashtag_one)
        except Exception as e:
            raise CommandError('Error updating data from twitter: "%s"' % e.__str__)
            
        contest.hashtag_one_typos = count_typos(hashtag_one_data)

        try:
            #Search for tweets from the second hashtag and process them
            hashtag_two_data = twitter.search.tweets(q="#"+contest.hashtag_two)
        except Exception as e:
            raise CommandError('Error updating data from twitter: "%s"' % e.message)

        contest.hashtag_two_typos = count_typos(hashtag_two_data)
        
        
        #We're using timezone.now() instead of datetime.now() in order to ensure that they are both timezone-aware
        if (timezone.now()>contest.end_date):
            contest.finished = True
            if contest.hashtag_one_typos<contest.hashtag_two_typos:
                contest.winner = 1
            elif contest.hashtag_one_typos>contest.hashtag_two_typos:
                contest.winner = 2
        contest.save()
    print("Contest update complete.")
