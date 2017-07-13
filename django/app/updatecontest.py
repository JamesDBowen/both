from django.core.management.base import BaseCommand, CommandError
from models import Contest
import twitter
import pyenchant

def count_typos(twitter_data):
    typos = 0
    for item in twitter_data.split(" "):
        typos += item.spellcheck()
    return typos

class Command(BaseCommand):
    help = 'Updates the battle of the hashtag contest'
    

    def handle(self, *args, **options):
        #Connects to the twitter search API
        twitter = Twitter(auth=oauth)
        for contest in Contest.filter(finished=False):
            try:
            # Search for tweets from the first hashtag and process them
            hashtag_one_data = twitter.search.tweets(q='#'+contest.hashtag_one)
            contest.hashtag_one_typos += count_typos(hashtag_one_data)

            #Search for tweets from the second hashtag and process them
            hashtag_two_data = twitter.search.tweets(q='#'+contest.hashtag_two)
            contest.hashtag_two_typos += count_typos(hashtag_two_data)
            
            contest.open0ed = False
            contest.save

            except Exception as e:
                raise CommandError('Error updating data from twitter: "%s"' % e.message)
