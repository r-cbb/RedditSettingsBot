#Example Credentials file.  Script uses credentials.py

#User 1
USERONE={'app_ua':'App User Agent Example',
    'app_id':'1234567890ABCD',
    'app_secret':'1234567890ABCDEFGHIJKLMNOPQ',
    'app_refresh':'1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ123'}
# app_scopes = ['identity','history','modconfig','read','wikiedit','wikiread']

#User 2
USERTWO={'app_ua':'App User Agent Example',
    'app_id':'1234567890ABCD',
    'app_secret':'1234567890ABCDEFGHIJKLMNOPQ',
    'app_refresh':'1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ123'}
# app_scopes = ['identity','flair','modflair','modposts','submit','edit','privatemessages']

def username(index):
    if index == 1:
        return USERONE
    elif index == 2:
        return USERTWO