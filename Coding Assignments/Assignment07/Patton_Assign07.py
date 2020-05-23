#  Author: Brandon Patton
#  Assignment 07 - Using the Twitter API to	access Twitter Data
#  This program accesses data from a twitter user site when given a users screen name
#  Input 'STOP' to cease process

#  To run in a terminal window:   py -3 Patton_Assign07.py OR python3 Patton_Assign07.py


import tweepy

### PUT AUTHENTICATION KEYS HERE ###
CONSUMER_KEY = "oZ63hBkwmJ8g5mnAMJlvUXuUs"
CONSUMER_KEY_SECRET = "fARQ1EOsyjHh0s7SxL2V5f9NXymaO6vTOMrPLlgIbb737PcaID"
ACCESS_TOKEN = "1248712305237528584-y52q75VxRWct0ZL49OngisQEuWUrRA"
ACCESS_TOKEN_SECRET = "KsSZQmAoeDl8rxeX9YXOQLeXTNWkokDPPoNR6OsaMDU6X"

def main():
    authenticate = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
    authenticate.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(authenticate, wait_on_rate_limit=True, 
                 wait_on_rate_limit_notify=True)

#borrowed the above code and formatting from the twitter_data.py file provided

    while (True):
        print("Please input a Twitter User Screen Name (Input STOP to cease process): ") 
        screen_Name = input()               #ask for input, collect with input()
        if (screen_Name == "STOP"):
                break
        twitter_user = api.get_user(screen_Name)        #set up user object with api
        print("\nUser Name: ", twitter_user.name)       #display user name with name attribute of user object
        print("User Screen Name: ", screen_Name)        #display screen name with inputted screen name
        print("User ID: ", twitter_user.id)             #display user id with id attribute of user object
        print("User Description: ", twitter_user.description)   #display user description with description attribute of user object
        first_10_fols = []
        followed_user = None
        follower_ids = api.followers_ids(screen_Name)       #get list of follower ids using the api method follower_ids
        for j in follower_ids:                              #loop through follower ids, collect first 10 followers
            if (len(first_10_fols) < 10):
                followed_user = api.get_user(j)             #get specific user from current id
                first_10_fols.append(followed_user.screen_name)
        print("Number of Followers: ", twitter_user.followers_count)        #display follower count with followers_count attribute of user object
        most_recent_id = api.user_timeline(screen_Name, count = 1)[0].id       #get the id of the most recent tweet using the api.user_timeline method
        print("Most Recent Tweet: ", api.get_status(most_recent_id, tweet_mode = 'extended')._json['full_text'])    #display text of most recent tweet using api.get_status method and setting flag tweet_mode to 'extended' to prevent truncation
        print("First 10 Followers: ", first_10_fols)        #display first 10 followers collected earlier 
    print("STOP was inputted, program has been stopped.")       #displays this message if the user inputs STOP when prompted for input.

main()