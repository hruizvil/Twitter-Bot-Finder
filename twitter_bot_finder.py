import tweepy
import datetime
import time

# Access codes from Twitter
consumerkey = ''
consumersecret = ''
accesstoken = ''
accesstokensecret = ''

# Create API handle
auth = tweepy.OAuthHandler(consumerkey, consumersecret)
auth.set_access_token(accesstoken, accesstokensecret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def twitter_bot_finder(user):
    '''
    This function automatically identifies up to 40 follow-bots 
    for any given Twitter account.
    '''
    # Limit on how many followers a bot account could have. 
    # I.e., 5 followers
    followers_limit = 5
    
    # Limit on how many accounts the bot account could be following. 
    # I.e., Following at most 10 accounts
    friends_limit = 20
    
    # Limit on how many tweets the bot account has posted.
    tweets_limit = 5
    
    # Obtains the current time
    now = datetime.datetime.now()
    # Modifies the time, so that we can limit the date under which the bot account should have been created
    date_limit = now.replace(year=2019, month=7, day=1, hour=0, minute=0, second=1) 
    
    # Obtains information about the specified user
    user = api.get_user(user)
    
    # Used to count the number of bot accounts found
    counter = 0
    
    # This for loop is used to create the script of finding one or more bot accounts
    for follower in user.followers():
        print('Examining @{}...'.format(follower.screen_name))
        # Checks if the amount of followers an account has falls under the "bot" category
        follower_count_under_limit = follower.followers_count < followers_limit
        # Checks if the amount of people an account is following falls under the "bot" category
        friends_count_under_limit = follower.friends_count < friends_limit
        # Checks if the amount of tweets an account has made falls under the "bot" category  
        status_count_under_limit = follower.statuses_count < tweets_limit
        # Checks if an account was created after the date_limit
        account_created_at_under_limit = follower.created_at > date_limit 
        
        # follower.default_profile_image checks if the user has a default profile image
        # If all conditions are met, this follower will be identified as a bot 
        if follower.default_profile_image and follower_count_under_limit and friends_count_under_limit and status_count_under_limit and account_created_at_under_limit:
            counter += 1
            print('Found follow-bot #{}: twitter.com/{}'.format(counter, follower.screen_name))
    
    # Used between network calls to avoid hitting the API limit
    time.sleep(60)

if __name__ == '__main__':
    twitter_bot_finder('realDonaldTrump')
