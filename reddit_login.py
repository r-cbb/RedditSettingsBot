import praw
import credentials

def scriptlogin(user):
    try:
        r = login(user)
        return r
    except:
        print("Failed to Login")
        raise

def login(user):
    activeuser = credentials.username(user)
    
    r = praw.Reddit(client_id=activeuser['app_id'],client_secret=activeuser['app_secret'],refresh_token=activeuser['app_refresh'],user_agent=activeuser['app_ua'])
    
    return r