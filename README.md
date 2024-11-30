# RedditSettingsBot
Automatically Updates the sidebar and posts Top 25 Rankings

Overview of files:
- `cbbpolldata.py`: Gets r/CollegeBasketball ranking
- `credentials_example `: Example File for reddit credentials.  Follow Reddit OAuth.  Built for 2 different accounts.
- `reddit_login.py `: Login to Reddit
- `requirements.txt`: Current Dependencies
- `scorebot_config`: Downloaded from https://www.reddit.com/r/CollegeBasketball/wiki/config_scorebot. Requirements of usual changes.
- `sidebar.py`: Main script ran.  Normally ran every 3 minutes during the season.

- `top25post.py:`: Posts the top 25 on a post when pulled.
- `top25update.py`: Updates the top 25 log weekly.  Limits pulls to only once a week.

- `data/headerranking.txt`: Storage of top 25 header
- `data/nond1_list.txt`: Used when wanting to verify if a team is missing.  Commented out in sidebar.py
- `data/ranking.txt`: Storage Location of /r/collegebasketball Rankings
- `data/team_list.txt`: List of teams with their ESPN tean name, flair, cbbpoll.com name, and Kenpom name.

Special Thanks to ischmidt20 for inspirations of various improvements and additional updates.
