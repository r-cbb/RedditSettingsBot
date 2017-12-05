import praw
import credentials

def login():
	r = praw.Reddit(client_id=credentials.app_id,client_secret = credentials.app_secret, refresh_token=credentials.app_refresh,user_agent=credentials.app_ua)
	return r