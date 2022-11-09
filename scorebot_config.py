# This includes everything before the top 25 on the sidebar.
PreTop25 = """ | | | | | | | | | |
---|---|----|----|----|----|----|----|----|----
[](/r/collegebasketball) |  | [](https://www.reddit.com/hot) |  | [](/r/collegebasketball) | [](/r/collegebasketball) | | [](https://www.reddit.com/hot) |  | [](/r/collegebasketball)
[](/r/collegebasketball) | | [](https://www.reddit.com) | | [](/r/collegebasketball) | [](/r/collegebasketball) | | [](https://www.reddit.com) | | [](/r/collegebasketball)
[](/r/collegebasketball) | | [](https://www.reddit.com) | | [](/r/collegebasketball/new) | [](/r/collegebasketball) |  | [](https://www.reddit.com) | | [](/r/collegebasketball)

#### 

###[Select Flair](/r/collegebasketball/wiki/flair)
###[Subreddit Rules](/r/collegebasketball/wiki/rules_guidelines)
###[Create a Game Thread](/r/collegebasketball/comments/5o5at9/introducing_ucbbbot_an_easier_way_of_making_game/)
###[Join us on Discord](https://discord.gg/redditcbb) [](#l/discord)
###[Follow us on Twitter](https://twitter.com/redditCBB) [](#l/twitter)
| | | | |
:--:|:--:|:---|:---
[User Poll](http://cbbpoll.com/)|
Rank||Team (FPV)|Score"""

# This is just a writer for the Sidebar Schedule.
BetweenTop25andSchedule = """

| | | | | |
:--:|:--:|:---:|:---:|:---:
Game Schedule|
Time (EsT) | Home | Away | TV | Score
"""

# This includes everything post Schedule.
PostTop25Header = """
##Resources##
  
#**Useful Links**

[Twitter (@redditCBB)](https://twitter.com/redditCBB)  
[Daily Schedule (ESPN)](http://espn.go.com/mens-college-basketball/schedule)  
[/r/CollegeBasketball Bracket Challenge](https://brackets.qxlp.net/)  

#**Subreddit Tools**

[/r/CollegeBasketball wiki](/r/CollegeBasketball/wiki/index)    
[Subreddit Rules](/r/CollegeBasketball/wiki/rules_guidelines)  
[Inline Flair](/r/CollegeBasketball/wiki/inlineflair)  

#**Archives**

[AMA Archive](/r/collegebasketball/search?q=flair%3A%27ama%27&sort=new&restrict_sr=on)  
[Game Thread Archive](/r/CollegeBasketball/search?q=flair%3A%27game+thread%27&restrict_sr=on&sort=new&t=all)  
[Trash Talk Archive](/r/CollegeBasketball/search?q=flair%3A%27trash+talk%27&restrict_sr=on&sort=new&t=all)  
[Announcements Archive](/r/collegebasketball/search?q=flair%3A%27modpost%27&sort=new&restrict_sr=on)  

#**Other**

[New to reddit? Click here!](/wiki/reddit_101)  
[kenpom.com](http://kenpom.com/)  
[ESPN](http://www.espn.com/)


##Related Subreddits##
#[Specific Schools/Conferences](/r/CollegeBasketball/wiki/relatedsubreddits)
#/r/ncaaBballstreams  
#/r/sports  
#/r/nba  
#/r/wnba  
#/r/cbbcirclejerk  
#/r/CFB  
#/r/CollegeBaseball  
#/r/CollegeSoccer  
#/r/NCAAW  
#/r/BracketChallenge  
#/r/ea2kcbb  
#/r/HSbball"""

# All Media flairs can be found here.
tv_flairs={'BTN':'[](#l/btn)','CBS':'[](#l/cbs)','CBSSN':'[](#l/cbssn)','ESPN':'[](#l/espn)','ESPN2':'[](#l/espn2)','ESPN3':'[](#l/espn3)','ESPNU':'[](#l/espnu)','ESPNN':'[](#l/espnews)','FOX':'[](#l/fox)','FS1':'[](#l/fs1)','FS2':'[](#l/fs2)','FSN':'[](#l/fsn)','Longhorn Network':'[](#l/lhn)','NBC':'[](#l/nbc)','NBCSN':'[](#l/nbcsn)','PAC12':'[](#l/p12n)','SECN':'[](#l/secn)','SECN+':'[](#l/secn)','TBS':'[](#l/tbs)','TNT':'[](#l/tnt)','truTV':'[](#l/trutv)','ACCNE':'[](#l/accne)'}

# Custom Top 25 Bar strings here.
top25barflag = 0 # 0 uses top 25 scraped from cbbpoll.com, 1 uses days till tipoff, 2 uses days,hours till tipoff, 3 uses custom string below
top25customstring = "####Wear a Mask! \n"

#Change the max length of the schedule.  6250 leaves ~50 characters for use.  
maxlength = 6250