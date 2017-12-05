from urllib.request import urlopen, Request
import json
import time
from fake_useragent import UserAgent
import html
import obot_cinciforthewin
import urllib.request
import shutil
import os
import re

PreTop25 = """ | | | | | | | | | |
---|---|----|----|----|----|----|----|----|----
[](https://www.reddit.com/r/cbbprivateflairtest) | | [](https://www.reddit.com) | | [](https://www.reddit.com/r/cbbprivateflairtest) | [](https://www.reddit.com/r/cbbprivateflairtest) | | [](https://www.reddit.com) | | [](https://www.reddit.com/r/cbbprivateflairtest)
[](https://www.reddit.com/r/cbbprivateflairtest) | | [](https://www.reddit.com) | | [](https://www.reddit.com/r/cbbprivateflairtest) | [](https://www.reddit.com/r/cbbprivateflairtest) | | [](https://www.reddit.com) | | [](https://www.reddit.com/r/cbbprivateflairtest)
[](https://www.reddit.com/r/cbbprivateflairtest) | | [](https://www.reddit.com) | | [](https://www.reddit.com/r/cbbprivateflairtest) | [](https://www.reddit.com/r/cbbprivateflairtest) | | [](https://www.reddit.com) | | [](https://www.reddit.com/r/cbbprivateflairtest)

#### 

###[Select Flair](/r/cbbprivateflairtest/wiki/flair)
###[Subreddit Rules](https://www.reddit.com/r/cbbprivateflairtest/wiki/rules_guidelines)
###[Create a Game Thread](https://www.reddit.com/r/cbbprivateflairtest/comments/5o5at9/introducing_ucbbbot_an_easier_way_of_making_game/)
###[Join us on Discord](https://discord.gg/74Bswry)
| | | | |
:--:|:--:|:---|:---
[User Poll](http://cbbpoll.com/)|
Rank||Team (FPV)|Score"""

top25string = """
#1|[](#f/duke)|Duke (43)|2055
#2|[](#f/michiganstate)|Michigan State (20)|1952
#2|[](#f/arizona)|Arizona (17)|1952
#4|[](#f/kansas)|Kansas (3)|1902
#5|[](#f/villanova)|Villanova |1748
#6|[](#f/wichitastate)|Wichita State (1)|1615
#7|[](#f/florida)|Florida |1447
#8|[](#f/northcarolina)|North Carolina |1409
#9|[](#f/kentucky)|Kentucky |1389
#10|[](#f/usc)|USC |1333
#11|[](#f/cincinnati)|Cincinnati |1219
#12|[](#f/miami)|Miami (FL) |1122
#13|[](#f/notredame)|Notre Dame |991
#14|[](#f/texasam)|Texas A&M |939
#15|[](#f/xavier)|Xavier |857
#16|[](#f/minnesota)|Minnesota |700
#17|[](#f/purdue)|Purdue |689
#18|[](#f/louisville)|Louisville |682
#19|[](#f/gonzaga)|Gonzaga (1)|662
#20|[](#f/setonhall)|Seton Hall |427
#21|[](#f/westvirginia)|West Virginia |410
#22|[](#f/stmarys)|St. Mary's |378
#23|[](#f/northwestern)|Northwestern |307
#24|[](#f/baylor)|Baylor |280
#25|[](#f/ucla)|UCLA |261"""

BetweenTop25andSchedule = """

| | | | | |
:--:|:--:|:---:|:---:|:---:
Schedule|
Time (EsT) | Home | Away | TV | Score
"""

Top25Header = """

#### [](#f/duke) [](#f/michiganstate) [](#f/arizona) [](#f/kansas) [](#f/villanova) [](#f/wichitastate) [](#f/florida) [](#f/northcarolina) [](#f/kentucky) [](#f/usc) [](#f/cincinnati) [](#f/miami) [](#f/notredame) [](#f/texasam) [](#f/xavier) [](#f/minnesota) [](#f/purdue) [](#f/louisville) [](#f/gonzaga) [](#f/setonhall) [](#f/westvirginia) [](#f/stmarys) [](#f/northwestern) [](#f/baylor) [](#f/ucla)
"""

PostTop25Header = """
##Resources##
  
#**Useful Links**

[Twitter (@redditCBB)](https://twitter.com/redditCBB)  
[Daily Schedule (ESPN)](http://espn.go.com/mens-college-basketball/schedule)  
[/r/CollegeBasketball Bracket Challenge](https://brackets.qxlp.net/)  

#**Subreddit Tools**

[/r/CollegeBasketball wiki](https://www.reddit.com/r/CollegeBasketball/wiki/index)    
[Subreddit Rules](https://www.reddit.com/r/CollegeBasketball/wiki/rules_guidelines)  
[Inline Flair](https://www.reddit.com/r/CollegeBasketball/wiki/inlineflair)  

#**Archives**

[AMA Archive](http://www.reddit.com/r/collegebasketball/search?q=flair%3A%27ama%27&sort=new&restrict_sr=on)  
[Game Thread Archive](https://www.reddit.com/r/CollegeBasketball/search?q=flair%3A%27game+thread%27&restrict_sr=on&sort=new&t=all)  
[Trash Talk Archive](https://www.reddit.com/r/CollegeBasketball/search?q=flair%3A%27trash+talk%27&restrict_sr=on&sort=new&t=all)  
[Announcements Archive](http://www.reddit.com/r/collegebasketball/search?q=flair%3A%27modpost%27&sort=new&restrict_sr=on)  

#**Other**

[New to reddit? Click here!](/wiki/reddit_101)  
[kenpom.com](http://kenpom.com/)  
[ESPN](http://www.espn.com/)


##Related Subreddits##
#[Specific Schools/Conferences](http://www.reddit.com/r/CollegeBasketball/wiki/relatedsubreddits)
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

tv_flairs={'BTN':'[](#f/btn)','CBS':'[](#f/cbs)','CBSSN':'[](#f/cbssn)','ESPN':'[](#f/espn)','ESPN2':'[](#f/espn2)','ESPN3':'[](#f/espn3)','ESPNU':'[](#f/espnu)','FOX':'[](#f/fox)','FS1':'[](#f/fs1)','FSN':'[](#f/fsn)','Longhorn Network':'[](#f/lhn)','NBC':'[](#f/nbc)','NBCSN':'[](#f/nbcsn)','PAC12':'[](#f/p12n)','SECN':'[](#f/secn)','SECN+':'[](#f/secn)','TBS':'[](#f/tbs)','TNT':'[](#f/tnt)','truTV':'[](#f/trutv)'}

def scriptlogin():
	r = obot_cinciforthewin.login()
	return r
	
def get_teams():
  with open('team_list.txt','r') as imp_file:
    lines=imp_file.readlines()
  flairs={}
  rank_names={}
  for line in lines:
    (team,flair,rank_name)=line.replace('\n','').split(',')
    flairs[team]=flair
    rank_names[rank_name]=team
  return flairs,rank_names

def get_rcbb_poll():
	(flairs,rank_names)=get_teams()
	url='http://cbbpoll.com/'
	with urllib.request.urlopen(url) as response, open ('ranking.html', 'wb') as out_file:
		shutil.copyfileobj(response, out_file)
	with open('ranking.html','r') as imp_file:
		lines=imp_file.readlines()
	ranking,headerranking,first_place_votes=[],[],[]
	i=1
	while i<125:
		first_place_votes.append('('+str(i)+')')
		i=i+1

	for line in lines:
		if "<td><span class='team-name'>" in line:
			# Rank
			team_rank=lines[lines.index(line)-1].replace('<td>','').replace('</td>','')
			# Team, FPV
			line=line.replace('&#39;',"'").replace('&#38;','&')
			begin=line.find('></span>')
			end=line.find('</span></td>')
			team=line[begin+9:end]
			for vote in first_place_votes:
				if vote in team:
					team=team.replace(vote,'')
					team_fpv=vote
					break
			# Votes
			team_vote=lines[lines.index(line)+1].replace('<td>','').replace('</td>','')
			
			ranking.append("#"+str(int(team_rank))+"|"+flairs[rank_names[team.replace('&amp;','&')]]+"|"+team.replace('&amp;','&')+" "+team_fpv+"|"+str(int(team_vote)))
			
			headerranking.append(flairs[rank_names[team.replace('&amp;','&')]])
			
		os.remove('ranking.html')
		with open('ranking.txt','w') as f:
			for team in ranking:
				f.write(team+'\n')
		
		with open('headerranking.txt','w') as f:
			for team in headerranking:
				if team == headerranking[-1]:
					f.write(team)
				else:
					f.write(team+' ')

def getrankings():
	with open('ranking.txt','r') as imp_file:
		lines=imp_file.readlines()
	sidebarrankings='\n'
	for line in lines:
		sidebarrankings += line
	return sidebarrankings
		
def getheaderrankings():
	with open('headerranking.txt','r') as imp_file:
		lines=imp_file.readlines()
	headerranking='#### '
	for line in lines:
		headerranking += line
	return headerranking
	
def getheaderrankingslist():
	with open('headerranking.txt','r') as imp_file:
		lines=imp_file.readlines()
	flairs = lines[0].split(' ')
	ranking = []
	i = 1
	while i<26:
		ranking.append(str(i))
		i=i+1
	n = 0
	rankings={}
	for flair in flairs:
		rankings[flair]=str(ranking[n])
		n=n+1
	return rankings
				
def updateschedule():

	MODE_ACTIVE = 0
	MODE_INACTIVE = 1
	GAME_STATUS_PRE = 0
	GAME_STATUS_IN = 1
	GAME_STATUS_POST = 2
	
	req = Request("http://www.espn.com/mens-college-basketball/scoreboard/_/group/50/?t=" + str(time.time()))
	req.headers["User-Agent"] = UserAgent(verify_ssl=False).chrome

	# Load data
	scoreData = urlopen(req).read().decode("utf-8")
	scoreData = scoreData[scoreData.find('window.espn.scoreboardData 	= ')+len('window.espn.scoreboardData 	= '):]
	scoreData = json.loads(scoreData[:scoreData.find('};')+1])

	games = dict()
	
	allgamestr = ''
	
	for event in scoreData['events']:
		game = dict()

		game["date"] = event['date']
		status = event['status']['type']['state']
		if status == "pre":
			game['status'] = GAME_STATUS_PRE
		elif status == "in":
			game['status'] = GAME_STATUS_IN
		else:
			game['status'] = GAME_STATUS_POST
			
		team1 = html.unescape(event['competitions'][0]['competitors'][0]['team']['location'])
		tid1 = event['competitions'][0]['competitors'][0]['id']
		score1 = int(event['competitions'][0]['competitors'][0]['score'])
		team1abv = event['competitions'][0]['competitors'][0]['team']['abbreviation']
		team2 = html.unescape(event['competitions'][0]['competitors'][1]['team']['location'])
		tid2 = event['competitions'][0]['competitors'][1]['id']
		score2 = int(event['competitions'][0]['competitors'][1]['score'])
		team2abv = event['competitions'][0]['competitors'][1]['team']['abbreviation']

		# Hawaii workaround
		if team1 == "Hawai'i":
			team1 = "Hawaii"
		if team2 == "Hawai'i":
			team2 = "Hawaii"

		homestatus = event['competitions'][0]['competitors'][0]['homeAway']

		if homestatus == 'home':
			game['hometeam'], game['homeid'], game['homeabv'], game['homescore'], game['awayteam'], game['awayid'], game['awayabv'], game['awayscore'] =\
				team1, tid1, team1abv, score1, team2, tid2, team2abv, score2
		else:
			game['hometeam'], game['homeid'], game['homeabv'], game['homescore'], game['awayteam'], game['awayid'], game['awayabv'], game['awayscore'] = \
				team2, tid2, team2abv, score2, team1, tid1, team1abv, score1

		game['time'] = event['status']['type']['shortDetail']
		
		if game['status'] == GAME_STATUS_PRE:
			searchedstring = re.search(' - (.*) EST',game['time'])
			gametime = searchedstring.group(1)
		elif game['status'] == GAME_STATUS_IN and game['time'] != "Halftime" and game['time'] != "Delayed":
			gametime = game['time'].replace(" - "," (") + ")"
		else:
			gametime = game['time']
		
		(teams,rank_names)=get_teams()
		teamranking = getheaderrankingslist()
		if team1 in teams.keys():
			team1flair = teams[team1]
		else:
			team1flair = "Non D1"
			# team1flair = team1
				
		if team1flair in teamranking.keys():
			team1flair = "^#"+str(teamranking[team1flair])+' '+team1flair
			
		if team2 in teams.keys():
			team2flair = teams[team2]
		else:
			team2flair = "Non D1"
			# team2flair = team2
		
		if team2flair in teamranking.keys():
			team2flair = "^#"+str(teamranking[team2flair])+' '+team2flair
		
		gamestring = gametime + " | " + team1flair + " | " + team2flair + " | "

		try:
			game['network'] = event['competitions'][0]['broadcasts'][0]['names'][0]
			
			if game['network'] in tv_flairs.keys():
				networkstring=tv_flairs[game['network']]
			else:
				networkstring=game['network']
			
			gamestring += networkstring + " | "
			
			# gamestring += game['network'] + " | "
			
		except:
			gamestring += " | "
			
		gamestring += str(score1) + "-" + str(score2)
		
		allgamestr += gamestring + '\n'
		
	return allgamestr

def updatesidebar():
	r = scriptlogin()
	# allgamestr = updateschedule()
	# top25string
	# Top25Header
	
	sidebarstring = PreTop25 + getrankings() + BetweenTop25andSchedule + updateschedule() + getheaderrankings() + PostTop25Header
	
	r.subreddit('cbbprivateflairtest').mod.update(description=sidebarstring)
	
# updatesidebar()
